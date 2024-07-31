import time
import copy

from .voyager import Voyager
from .agents import Developer, Evaluator
from .agents import Patroller


class CustomVoyager(Voyager):
    def __init__(self, **kwargs):
        super().__init__(
            openai_api_key=kwargs["openai_api_key"],
            skill_library_dir=kwargs["skill_library_dir"],
            ckpt_dir=kwargs['ckpt_dir'],
            mc_port=kwargs["mc_port"],
        )
        self.developer = Developer(
            model_name=kwargs['developer_model_name'],
            temperature=kwargs['developer_template'],
            request_timeout=kwargs['openai_api_request_timeout'],
        )

        self.patroller = Patroller(
            model_name=kwargs['patroller_model_name'],
            temperature=kwargs['patroller_template'],
            request_timeout=kwargs['openai_api_request_timeout'],
        )

        self.evaluator = Evaluator(
            model_name=kwargs['evaluator_model_name'],
            temperature=kwargs['evaluator_template'],
            request_timeout=kwargs['openai_api_request_timeout'],
        )

        self.task =  None



    def reset(self, task, context="", criteria='', reset_env=True):
        self.action_agent_rollout_num_iter = 0
        self.task = task
        self.criteria = criteria
        self.skill = None
        self.context = context
        if reset_env:
            self.env.reset(
                options={
                    "mode": "soft",
                    "wait_ticks": self.env_wait_ticks,
                }
            )
        difficulty = ("peaceful")
        events = self.env.step(
            "bot.chat(`/time set ${getNextTime()}`);\n"
            + f"bot.chat('/difficulty {difficulty}');"
        )
        #TODO : returieve_skills 변경 필요
        #TODO : skills가 program_code, program_name, exec_code key 가지도록
        skills = self.skill_manager.retrieve_skills(query=self.context)
        print(
            f"\033[33mRender Action Agent system message with {len(skills)} skills\033[0m"
        )
        # if not skill:
        system_message = self.developer.render_system_message(skills=skills)
        human_message = self.developer.render_human_message(
            events=events, code="", task=self.task, context=context, evaluation=""
        )

        self.messages = [system_message, human_message]
        print(
            f"\033[32m****Action Agent human message****\n{human_message.content}\033[0m"
        )
        assert len(self.messages) == 2
        self.conversations = []
        return self.messages
        # else:
        #     print(
        #         f"\033[32m****Has skill already made ****\n\033[0m"
        #     )
        #     self.skill = skill
        #     self.messages = None
        #     return self.messages


    def rollout(self, *, task, context, criteria, reset_env=True):
        self.reset(task=task, context=context, criteria=criteria, reset_env=reset_env)
        while True:
            message, done, info = self.step()
            if done:
                break

        return message, done, info

    def step(self):
        if self.action_agent_rollout_num_iter < 0:
            raise ValueError("Agent must be reset before stepping")
        if self.messages:
            ai_message = self.developer.llm(self.messages)
            print(f"\033[34m****Action Agent ai message****\n{ai_message.content}\033[0m")
            self.conversations.append(
                (self.messages[0].content, self.messages[1].content, ai_message.content)
            )
            message = self.action_agent.process_ai_message(message=ai_message)
            parsed_result = message
        else:
            # 실행 가능한 js code로, exec code 생성
            parsed_result = self.action_agent.process_skill(self.skill)
        success = False
        if isinstance(parsed_result, dict):
            code = parsed_result["program_code"] + "\n" + parsed_result["exec_code"]
            # 환경에서 code 실행 -> monitor 요소도 넘겨서 발견시 stop하게 하자
            events = self.env.step(  # 게임에서 스탭
                code,
                programs=self.skill_manager.programs,
                criteria=self.criteria
            )
            self.recorder.record(events, self.task)
            self.action_agent.update_chest_memory(events[-1][1]["nearbyChests"])
            # success, critique = self.critic_agent.check_task_success(
            #     events=events,
            #     task=self.task,
            #     context=self.context,
            #     chest_observation=self.action_agent.render_chest_observation(),
            #     max_retries=5,
            # )
            success, critique = self.evaluator.evaluate_situation(
                events=events,
                task=self.task,
                context=self.context,
            )

            system_message = self.developer.render_system_message(skills=parsed_result["program_code"])
            human_message = self.developer.render_human_message(
                events=events,
                code=parsed_result["program_code"],
                task=self.task,
                context=self.context,
                evaluation=critique,
            )
            self.last_events = copy.deepcopy(events)
            self.messages = [system_message, human_message]
        else:
            assert isinstance(parsed_result, str)
            self.recorder.record([], self.task)
            print(f"\033[34m{parsed_result} Trying again!\033[0m")
        assert len(self.messages) == 2
        self.action_agent_rollout_num_iter += 1
        done = (
                self.action_agent_rollout_num_iter >= self.action_agent_task_max_retries
                or success
        )
        info = {
            "task": self.task,
            "success": success,
            "conversations": self.conversations,
        }
        if success:
            assert (
                "program_code" in parsed_result and "program_name" in parsed_result
            ), "program and program_name must be returned when success"
            info["program_code"] = parsed_result["program_code"]
            info["program_name"] = parsed_result["program_name"]
        else:
            print(
                f"\033[32m****Action Agent human message****\n{self.messages[-1].content}\033[0m"
            )
        return self.messages, done, info

    def learn(self, reset_env = True):
        self.env.reset(
             options={
                "mode": "hard",
                "wait_ticks": self.env_wait_ticks,
            }
        )
        self.last_events = self.env.step("")
        while True:
            if self.recorder.iteration > self.max_iterations:
                print("Iteration limit reached")
                break

            # task, context = self.curriculum_agent.propose_next_manual_task_auto_context()
            task = 'get 1 wood'
            context = "Question: How to get 1 wood in Minecraft? \nAnswer: To get 1 wood in Minecraft, you can start by punching a tree. This will cause wood blocks to drop, which you can then collect by walking over them. Once you have collected the wood blocks, you can craft them into wooden planks by placing them in the crafting grid."

            criteria = self.patroller.select_monitor_factor(task, context, self.last_events)
            print(
                f"\033[35mStarting task {task} for at most {self.action_agent_task_max_retries} times\033[0m"
            )
            try:
                message, done, info = self.rollout(task=task, context=context, criteria=criteria, reset_env=reset_env)
            except Exception as e:
                time.sleep(3)  # wait for mineflayer to exit
                info = {
                    "task": task,
                    "success": False,
                }
                # reset bot status here
                self.last_events = self.env.reset(
                    options={
                        "mode": "hard",
                        "wait_ticks": self.env_wait_ticks,
                        "inventory": self.last_events[-1][1]["inventory"],
                        "equipment": self.last_events[-1][1]["status"]["equipment"],
                        "position": self.last_events[-1][1]["status"]["position"],
                    }
                )
                # use red color background to print the error
                print("Your last round rollout terminated due to error:")
                print(f"\033[41m{e}\033[0m")





if __name__ == '__main__':
    voyager = CustomVoyager()
    voyager.reset(task='find wood', reset_env=True)


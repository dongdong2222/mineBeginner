from datetime import time

from langchain_openai import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from ..prompts import load_prompt
from ..env import bridge

class Patroller:
    def __init__(
            self,
            model_name:str = "gpt-3.5-turbo",
            temperature:int = 0,
            request_timeout:int = 120,
            ckpt_dir:str = "ckpt",
            *,
            env = None,
            developer = None,
            # evaluator = None,
    ):
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
        )
        self.ckpt_dir = ckpt_dir
        self.env = env
        self.developer = developer
        # self.evaluator = evaluator
        self.monitoring_targets = {
            ### 작업 중간에 측정
            'dig_time': 0,
            'current_health': 0,
            'current_food': 0,
            'current_oxygen': 0,
            'current velocity': 0,
            'damage': 0,
            'elapsed_time': 0,
            ### 작업 완료 후 측정
            'collected_items':{},
            'used_items': {},
            'explored_distance': 0,
            'explored_depth': 0,

        }
        self.evaluation_criteria = {}
        pass

    def render_system_message(self, task):
        system_template = load_prompt("select_monitor_factor")
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        system_message = system_message_prompt.format(
            task=task,
        )
        assert isinstance(system_message, SystemMessage)
        return system_message

    def render_human_message(
            self, *, events, code="", task="", context="", critique=""
    ):
        chat_messages = []
        error_messages = []
        # FIXME: damage_messages is not used
        damage_messages = []
        assert events[-1][0] == "observe", "Last event must be observe"
        for i, (event_type, event) in enumerate(events):
            if event_type == "onChat":
                chat_messages.append(event["onChat"])
            elif event_type == "onError":
                error_messages.append(event["onError"])
            elif event_type == "onDamage":
                damage_messages.append(event["onDamage"])
            elif event_type == "observe":
                biome = event["status"]["biome"]
                time_of_day = event["status"]["timeOfDay"]
                voxels = event["voxels"]
                entities = event["status"]["entities"]
                health = event["status"]["health"]
                hunger = event["status"]["food"]
                position = event["status"]["position"]
                equipment = event["status"]["equipment"]
                inventory_used = event["status"]["inventoryUsed"]
                inventory = event["inventory"]
                assert i == len(events) - 1, "observe must be the last event"

        observation = ""

        if code:
            observation += f"Code from the last round:\n{code}\n\n"
        else:
            observation += f"Code from the last round: No code in the first round\n\n"

        # if self.execution_error:
        #     if error_messages:
        #         error = "\n".join(error_messages)
        #         observation += f"Execution error:\n{error}\n\n"
        #     else:
        #         observation += f"Execution error: No error\n\n"
        #
        # if self.chat_log:
        #     if chat_messages:
        #         chat_log = "\n".join(chat_messages)
        #         observation += f"Chat log: {chat_log}\n\n"
        #     else:
        #         observation += f"Chat log: None\n\n"

        observation += f"Biome: {biome}\n\n"

        observation += f"Time: {time_of_day}\n\n"

        if voxels:
            observation += f"Nearby blocks: {', '.join(voxels)}\n\n"
        else:
            observation += f"Nearby blocks: None\n\n"

        if entities:
            nearby_entities = [
                k for k, v in sorted(entities.items(), key=lambda x: x[1])
            ]
            observation += f"Nearby entities (nearest to farthest): {', '.join(nearby_entities)}\n\n"
        else:
            observation += f"Nearby entities (nearest to farthest): None\n\n"

        observation += f"Health: {health:.1f}/20\n\n"

        observation += f"Hunger: {hunger:.1f}/20\n\n"

        observation += f"Position: x={position['x']:.1f}, y={position['y']:.1f}, z={position['z']:.1f}\n\n"

        observation += f"Equipment: {equipment}\n\n"

        if inventory:
            observation += f"Inventory ({inventory_used}/36): {inventory}\n\n"
        else:
            observation += f"Inventory ({inventory_used}/36): Empty\n\n"

        # if not (
        #         task == "Place and deposit useless items into a chest"
        #         or task.startswith("Deposit useless items into the chest at")
        # ):
        #     observation += self.render_chest_observation()

        observation += f"Task: {task}\n\n"

        if context:
            observation += f"Context: {context}\n\n"
        else:
            observation += f"Context: None\n\n"

        if critique:
            observation += f"Critique: {critique}\n\n"
        else:
            observation += f"Critique: None\n\n"

        return HumanMessage(content=observation)



    def select_monitor_factor(self, task, context, events):
        system_message = self.render_system_message(task)
        human_message = self.render_human_message(
            events=events,
            code="",
            task=task,
            context=context,
        )
        print(
            f"\033[34m****Monitor factor system message****\n{system_message.content}\033[0m"
        )
        print(
            f"\033[32m****Monitor factor human message****\n{human_message.content}\033[0m"
        )
        message = [system_message, human_message]
        response = self.llm(message)

        test_res = {
            "health": ['less', 19.0]
        }
        return test_res
        # return response
        pass










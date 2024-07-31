
from langchain_openai import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from ..prompts import load_prompt
from voyager.test_control_primitives_context import load_test_control_primitives_context

class Developer:
    def __init__(
            self,
            model_name:str = "gpt-3.5-turbo",
            temperature:int = 0,
            request_timeout:int = 120,
            ckpt_dir:str = "ckpt"
    ):
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
        )
        self.ckpt_dir = ckpt_dir
        pass
    def render_system_message(self, skills=""):
        system_template = load_prompt("generate_skill")
        programs = "\n\n".join(load_test_control_primitives_context(["mineflayer"]))
        response_format = load_prompt("generate_skill_response")

        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        system_message = system_message_prompt.format(
            skills=skills, response_format=response_format,
        )
        assert isinstance(system_message, SystemMessage)
        return system_message

    def render_human_message(self, *, events, code, task, context, evaluation ):

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

        observation += f"Biome: {biome}\n\n"

        observation += f"Time: {time_of_day}\n\n"

        if voxels:
            observation += f"Nearby blocks: {', '.join(voxels)}\n\n"
        else:
            observation += f"Nearby blocks: None\n\n"

        return HumanMessage(content=observation)


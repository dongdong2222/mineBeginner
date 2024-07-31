
from langchain_openai import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import voyager.utils as U


from ..prompts import load_prompt

class Evaluator:
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

    def render_system_message(self):
        system_template = load_prompt("evaluate_skill")
        response_template =load_prompt("evaluate_skill_response")
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        system_message = system_message_prompt.format(
            response=response_template
        )
        assert isinstance(system_message, SystemMessage)
        return system_message

    def render_human_message(self, events, task, context):
        chat_messages = []
        error_messages = []
        damage_messages = []
        detect_messages = []

        assert events[-1][0] == "observe", "Last event must be observe"
        for i, (event_type, event) in enumerate(events):
            if event_type == "onChat":
                chat_messages.append(event["onChat"])
            elif event_type == "onError":
                error_messages.append(event["onError"])
            elif event_type == "onDetection":
                error_messages.append(event["onDetection"])
            elif event_type == "observe":
                # current state
                # biome = event['status'['biome']
                pass

        observation = ""







        return HumanMessage(content=observation)

    def evaluate_situation(self, *, event, task, context):
        system_message = self.render_system_message()
        human_message = self.render_human_message(event, task, context)
        message = [system_message, human_message]
        response = self.llm(message)
        response_dict = U.json_load(response.content)
        assert "success" in response_dict, "response don't have success key"
        assert "evaluation" in response_dict, "response don't have evaluation key"
        return response_dict['success'], response_dict['evaluation']
        pass



if __name__ == "__main__":
    evaluator = Evaluator()
    evaluator.select_monitor_factor(
        task="get 1 wood",
        context="Question: How to get 1 wood in Minecraft? \nAnswer: To get 1 wood in Minecraft, you can start by punching a tree. This will cause wood blocks to drop, which you can then collect by walking over them. Once you have collected the wood blocks, you can craft them into wooden planks by placing them in the crafting grid.",
        events=[["observe",{"voxels":["mangrove_leaves","vine","mangrove_propagule","mangrove_log"],"status":{"health":0,"food":20,"saturation":5,"position":{"x":-3.5,"y":77,"z":4.5},"velocity":{"x":0,"y":-0.0784000015258789,"z":0},"yaw":3.141592653589793,"pitch":0,"onGround":true,"equipment":[null,null,null,null,null,null],"name":"bot","isInWater":false,"isInLava":false,"isCollidedHorizontally":false,"isCollidedVertically":true,"biome":"mangrove_swamp","entities":{"tropical_fish":30.249129891489993,"zombie":31.500248014896645,"skeleton":29.086079144497972},"timeOfDay":"sunrise","inventoryUsed":0,"elapsedTime":0},"inventory":{},"nearbyChests":{},"blockRecords":[]}]]
    )
    pass
from .action import ActionAgent

from langchain.prompts import SystemMessagePromptTemplate
from langchain.schema import SystemMessage

from ..test_control_primitives_context import load_test_control_primitives_context
from ..prompts import load_prompt

class CustomActionAgent(ActionAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    #@overrides
    def render_system_message(self, skills=[]):
        #새로 만든 prompt로 변경하기
        system_template = load_prompt("action_template")
        # FIXME: Hardcoded control_primitives
        # test_control_primitives_context에 맞게 조정하기
        base_skills = [
            "exploreUntil",
            "mineBlock",
            "craftItem",
            "placeItem",
            "smeltItem",
            "killMob",
        ]
        # base_skills = [
        #     "moveBack",
        #     "moveForward",
        #     "moveLeft",
        #     "moveRight",
        #     "sneak",
        #     "sprint",
        # ]
        if not self.llm.model_name == "gpt-3.5-turbo":
            base_skills += [
                "useChest",
                "mineflayer",
            ]
        programs = "\n\n".join(load_test_control_primitives_context(base_skills) + skills)
        response_format = load_prompt("action_response_format")
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            system_template
        )
        system_message = system_message_prompt.format(
            programs=programs, response_format=response_format
        )
        assert isinstance(system_message, SystemMessage)
        return system_message

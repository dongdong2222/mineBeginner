from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from voyager.prompts import load_prompt

class BaseAgent:
    def __init__(
            self,
            model_name="gpt-3.5-turbo",
            temperature=0,
            request_timeout=120,
            ckpt_dir="ckpt"
            #mode="auto"
    ):
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
        )

    def render_system_message(self, f_prompt):
        system_message = SystemMessage(content=load_prompt(f_prompt))
        assert isinstance(system_message, SystemMessage), "system_message must be of type SystemMessage"
        return system_message

    def render_human_message(self, f_prompt):
        pass

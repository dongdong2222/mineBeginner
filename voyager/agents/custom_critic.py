from .critic import CriticAgent

class CustomCriticAgent(CriticAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
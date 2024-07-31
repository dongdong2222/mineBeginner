from .curriculum import CurriculumAgent

class CustomCurriculumAgent(CurriculumAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
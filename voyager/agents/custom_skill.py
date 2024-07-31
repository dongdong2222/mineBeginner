from .skill import SkillManager
from ..test_control_primitives import load_test_control_primitives

class CustomSkillManager(SkillManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.test_control_primitives = load_test_control_primitives()

    @property
    def programs(self):
        programs = ""
        for skill_name, entry in self.skills.items():
            programs += f"{entry['code']}\n\n"
        for primitive in self.test_control_primitives:
            programs += f"{primitive}\n\n"
        return programs

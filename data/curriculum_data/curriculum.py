import json
from data.curriculum_data.curriculum_helper_functions import load_curriculum_json

class Curriculum:
    def __init__(self):
        self.curriculum_dict = load_curriculum_json()

    def __str__(self):
        WIDTH = 40
        lines = []
        for part, rules in self.curriculum_dict["principal_parts"].items():
            header = f"┌─ {part.title()} "
            lines.append(header + "─" * (WIDTH - len(header)))
            for rule, forms in rules.items():
                forms_text = " · ".join(f"{f:<10}" for f in forms).rstrip()
                lines.append(f"│  {rule:<8} {forms_text}")
            lines.append("└" + "─" * (WIDTH - 1))
        return "\n".join(lines)



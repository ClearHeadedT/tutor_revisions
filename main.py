import json

from data.student_data.student import Student
from tasks.initial_card_creation.main import create_new_cards


LEXEMES = [
    ("ἄρτος", "ὁ ἄρτος"),
]


def run():
    student = Student("austin")
    new_cards = create_new_cards(lexemes=LEXEMES, student=student)
    return json.dumps(new_cards, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    print(run())

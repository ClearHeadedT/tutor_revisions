import json

from data.student_data.student import Student
from tasks.new_card_creation.main import create_new_vocabulary_cards


LEXEMES = [
    ("ἄρτος", "ὁ ἄρτος"),
]


def run():
    student = Student("austin")
    new_cards = create_new_vocabulary_cards(lexemes=LEXEMES, student=student, desired_card_type="text_recall_vocabulary_g2e")
    return json.dumps(new_cards, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    print(run())

import json

from data.student_data.student import Student
from tasks.new_card_creation.main import (
    create_new_vocabulary_cards,
    create_new_grammar_cards,
)


STUDENT_ID = "austin"

# (form Text-Fabric indexes, conventional lexicon entry)
LEXEMES = [
    ("ἄρτος", "ὁ ἄρτος"),
]

# slot keys from data/curriculum_data/grammar_scaffolding.json
GRAMMAR_ITEMS = [
    "decl2::λόγος::genitive.singular",
]

VOCABULARY_CARD_TYPE = "text_recall_vocabulary_g2e"
GRAMMAR_CARD_TYPE = "text_recall_grammar_g2e"


def run():
    student = Student(STUDENT_ID)
    new_cards = {
        "vocabulary": create_new_vocabulary_cards(
            lexemes=LEXEMES, student=student, desired_card_type=VOCABULARY_CARD_TYPE
        ),
        "grammar": create_new_grammar_cards(
            grammar_item_keys=GRAMMAR_ITEMS, student=student, desired_card_type=GRAMMAR_CARD_TYPE
        ),
    }
    return json.dumps(new_cards, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    print(run())

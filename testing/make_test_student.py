"""Writes data/student_data/test_student/, a realistic student for testing card generation.

    python -m testing.make_test_student

beyond_beginner, knowing the 500 commonest GNT words, every grammar form the scaffolding holds,
and the core syntax items together with every construction a sentence plan can offer - enough for
the vocabulary check to mean something and for plans to reach their full range. Rewriting it
empties its card history, which is what a test student should start from.
"""
import json
from datetime import date
from pathlib import Path

from data.student_data.student_data_helper_functions import (
    load_grammar_scaffolding,
    load_syntax_scaffolding,
    load_vocabulary_scaffolding,
)

STUDENT_ID = "test_student"
VOCABULARY_SIZE = 500
FOLDER = Path("data/student_data") / STUDENT_ID


def build():
    today = date.today().isoformat()
    learned = {"status": "learned", "last_reviewed": today}
    vocabulary = load_vocabulary_scaffolding()["items"]
    commonest = sorted(vocabulary, key=lambda lemma: -vocabulary[lemma]["frequency"])[:VOCABULARY_SIZE]
    wiring = json.loads(Path("data/curriculum_data/traversal_wiring.json").read_text(encoding="utf-8"))
    syntax = {usage["syntactic_item"] for usage in wiring.values()}
    syntax |= {key for key, item in load_syntax_scaffolding()["items"].items() if item.get("core")}
    return {
        "student_overview.json": {"student_id": STUDENT_ID, "level": "beyond_beginner"},
        "student_vocabulary_data.json": {"student_id": STUDENT_ID,
                                         "vocabulary": {lemma: learned for lemma in commonest}},
        "student_grammar_data.json": {"student_id": STUDENT_ID,
                                      "grammar": {key: learned for key in load_grammar_scaffolding()["items"]}},
        "student_syntax_data.json": {"student_id": STUDENT_ID,
                                     "syntax": {key: learned for key in sorted(syntax)}},
        "student_card_data.json": {"student_id": STUDENT_ID, "cards": {}},
    }


def write():
    FOLDER.mkdir(parents=True, exist_ok=True)
    for name, data in build().items():
        (FOLDER / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {name: len(next(v for k, v in data.items() if k != "student_id")) if len(data) > 1 else 0
            for name, data in build().items()}


if __name__ == "__main__":
    print(write())

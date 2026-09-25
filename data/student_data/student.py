from datetime import date

from data.curriculum_data.grammar_groups import all_groups, group_name, group_of
from data.student_data.student_data_helper_functions import (
    load_student_overview,
    load_student_grammar_data,
    load_student_vocabulary_data,
    load_student_syntax_data,
    load_student_card_data,
    load_vocabulary_senses,
    save_student_vocabulary_data,
    save_student_grammar_data,
    save_student_syntax_data,
    save_student_card_data,
    normalize_progress,
)


class Student:
    """Everything known about one student, loaded once and held. This is a container:
    it holds state and answers questions about it, while the work of building cards and
    running reviews lives in the task modules that take a Student.

    All of it loads in __init__, which costs well under a millisecond."""

    def __init__(self, student_id):
        self.student_id = student_id
        self.level = load_student_overview(student_id)["level"]
        self.grammar = normalize_progress(load_student_grammar_data(student_id)["grammar"])
        self.vocabulary = normalize_progress(load_student_vocabulary_data(student_id)["vocabulary"])
        self.syntax = normalize_progress(load_student_syntax_data(student_id)["syntax"])
        self.cards = normalize_progress(load_student_card_data(student_id)["cards"])
        self.senses = load_vocabulary_senses()

    def grammar_groups_learned(self):
        """The grammar groups the student can build from - a rule such as aor1-pas-ind, or a
        participle tense and voice - having met at least one slot of each. In curriculum order."""
        met = {group_of(key) for key in self.grammar}
        return [group for group in all_groups() if group in met]

    def concepts_learned(self):
        """What the student has covered, read off the progress files on each call so it always
        matches them. Grammar is named by group rather than listed by slot: the model needs to
        know that aorist passive participles are available, not which cells of the chart were
        reviewed."""
        return {"grammar": [group_name(group) for group in self.grammar_groups_learned()],
                "syntax": list(self.syntax)}

    def vocabulary_learned(self):
        return list(self.vocabulary)

    def student_overview(self):
        """Where this student currently stands, in the shape instructions_cap
        describes to the model as its "student" block."""
        return {
            "level": self.level,
            "concepts_learned": self.concepts_learned(),
            "vocabulary_learned": self.vocabulary_learned(),
        }

    def recent_generations(self, key, limit=3):
        """The cards already made for this item, which constraint 11 forbids the model
        from repeating. Trimmed to what it needs to avoid repeating, since the stored
        reasoning would otherwise fill most of the prompt."""
        history = self.cards.get(key, {}).get("card_history", [])[-limit:]
        return [{field: card[field] for field in ("card_type", "sentence", "translation")
                 if field in card} for card in history]

    def recent_settings(self, key, limit=3):
        """The scene-bank settings the last few cards for this item were built in, so the next
        plan can offer different ones."""
        history = self.cards.get(key, {}).get("card_history", [])[-limit:]
        return [card["setting"].removeprefix("adapted:") for card in history if card.get("setting")]

    def record_card(self, key, card, domain="vocabulary"):
        """Appends a generated card to this item's history, dated today. An item met for
        the first time starts as learning; one already being studied keeps the progress
        it has. domain is "vocabulary", "grammar" or "syntax"."""
        today = date.today().isoformat()
        progress = {"vocabulary": self.vocabulary, "grammar": self.grammar, "syntax": self.syntax}[domain]
        savers = {"vocabulary": save_student_vocabulary_data,
                  "grammar": save_student_grammar_data,
                  "syntax": save_student_syntax_data}
        progress.setdefault(key, {"status": "learning", "last_reviewed": today})
        savers[domain](self.student_id, {"student_id": self.student_id, domain: progress})
        self.cards.setdefault(key, {"card_history": []})["card_history"].append({"date": today, **card})
        save_student_card_data(
            self.student_id, {"student_id": self.student_id, "cards": self.cards}
        )

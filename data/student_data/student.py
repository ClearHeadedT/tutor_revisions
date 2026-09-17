from data.student_data.student_data_helper_functions import (
    load_student_overview,
    load_student_grammar_data,
    load_student_vocabulary_data,
    load_student_syntax_data,
    load_student_card_data,
    load_vocabulary_senses,
    save_student_vocabulary_data,
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

    def concepts_learned(self):
        """Every grammar and syntax key the student has met, read off the progress
        files on each call so it always matches them."""
        return list(self.grammar) + list(self.syntax)

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

    def record_new_vocabulary(self, lemma, reference_card, first_seen):
        """Adds a word the student has just met, with the reference card generated
        for it. Progress and cards are separate files, so both are written."""
        self.vocabulary[lemma] = {"status": "learning", "last_reviewed": first_seen}
        save_student_vocabulary_data(
            self.student_id, {"student_id": self.student_id, "vocabulary": self.vocabulary}
        )
        self.cards.setdefault(lemma, {"card_history": []})["reference_card"] = reference_card
        save_student_card_data(
            self.student_id, {"student_id": self.student_id, "cards": self.cards}
        )

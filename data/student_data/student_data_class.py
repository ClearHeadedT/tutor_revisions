from datetime import date
import json
from cards.vocabulary.vocabulary_cards import text_recall_vocabulary_g2e, cloze_vocabulary_e2g, cloze_vocabulary_e2g
from cards.grammar.grammar_cards import text_recall_grammar_g2e
from cards.syntax.syntax_cards import function_recall_syntax_g2e
from data.student_data.student_data_helper_functions import (
    load_grammar_scaffolding,
    load_vocabulary_scaffolding,
    load_syntax_scaffolding,
    load_student_grammar_data,
    load_student_vocabulary_data,
    load_student_syntax_data,
    load_student_card_data,
)



class StudentData:
    def __init__(self, student_id):
        self.student_id = student_id
        self.grammar_scaffolding = load_grammar_scaffolding()
        self.vocabulary_scaffolding = load_vocabulary_scaffolding()
        self.syntax_scaffolding = load_syntax_scaffolding()
        self.student_grammar_data = load_student_grammar_data(student_id=student_id)["grammar"]
        self.student_vocabulary_data = load_student_vocabulary_data(student_id=student_id)["vocabulary"]
        self.student_syntax_data = load_student_syntax_data(student_id=student_id)["syntax"]
        self.student_card_data = load_student_card_data(student_id=student_id)["cards"]
        self.student_cards_by_item = self.load_cards_for_items()


    def sort_items_by_status(self, scaffolding, progress):
        items_by_status = {
            "learned": {key: record for key, record in progress.items() if record["status"] == "learned"},
            "learning": {key: record for key, record in progress.items() if record["status"] == "learning"},
            "unseen": {key: {} for key in scaffolding["items"] if key not in progress}
        }
        return items_by_status


    def sort_by_review_date(self, scaffolding, progress, status="learned"):
        items_by_status = self.sort_items_by_status(scaffolding, progress)[status]
        today = date.today()
        day_data_reviews = {}
        for key, record in items_by_status.items():
            days_since_review = (today - date.fromisoformat(record["last_reviewed"])).days
            new_record = dict(record)
            new_record["prior_day_count"] = days_since_review
            day_data_reviews[key] = new_record
        return dict(sorted(day_data_reviews.items(), key=lambda x: x[1]["prior_day_count"]))


    def load_cards_for_items(self):
        cards_for_items = {}
        for item, _ in self.student_card_data.items():
            card_history_for_item = self.student_card_data[item]
            cards_for_items[item] = card_history_for_item
        return cards_for_items


    def _sort_item_into_c_difficulty(item):
        card_type = None
        if item["status"] == "learning":
            card_type = "text_recall_vocabulary_g2e"
        return card_type




class StudentGrammar(StudentData):
    def __init__(self, student_id):
        super().__init__(student_id)

    def sort_grammar_by_due_date(self):
        return sort_items_by_due_date(self.student_grammar_data)

    def initial_grammar_formulation(self):
        cards = []
        for _, internals in self.grammar_scaffolding["items"].items():
            cards.append(text_recall_grammar_g2e(internals))
        return(cards)



class StudentVocabulary(StudentData):
    def __init__(self, student_id):
        super().__init__(student_id)

    def sort_vocabulary_by_due_date(self):
        return sort_items_by_due_date(self.student_vocabulary_data)

    def vocabulary_review(self):
        for item, _ in self.sort_vocabulary_by_due_date().items():
            scaffolding_v_item = self.vocabulary_scaffolding["items"][item]
            card_history_v_item = self.student_vocabulary_data[item]
            print(scaffolding_v_item, "\n")

    def initial_vocabulary_formulation(self):
        cards = []
        for _, internals in self.vocabulary_scaffolding["items"].items():
            cards.append(text_recall_vocabulary_g2e(internals))
        return(cards)

    def _sort_vocabulary_review_austin(self, vocabulary_item_keys):
        for key in vocabulary_item_keys:
            history = self.student_cards_by_item[key]["card_history"]
            current_item = history[-1]
            if (current_item["status_at_review"] == "learning"
                and current_item["correct"] == False
                and current_item["card_type"] == "text_recall_vocabulary_g2e"):
                return text_recall_vocabulary_g2e
            elif (current_item["status_at_review"] == "learning"
                and current_item["correct"] == False
                and current_item["card_type"] == "cloze_vocabulary_e2g"
                and len(history) >= 2
                and history[-2]["correct"] == False):
                return text_recall_vocabulary_g2e
            else:
                return cloze_vocabulary_e2g
        




class StudentSyntax(StudentData):
    def __init__(self, student_id):
        super().__init__(student_id)

    def sort_syntax_by_due_date(self):
        return sort_items_by_due_date(self.student_syntax_data)

    def initial_syntax_formulation(self):
        cards = []
        for _, internals in self.syntax_scaffolding["items"].items():
            cards.append(function_recall_syntax_g2e(internals))
        return(cards)

    




def sort_items_by_due_date(items):
    today = date.today()
    day_data_reviews = {}
    for key, internals in items.items():
        days_since_review = (today - date.fromisoformat(internals["last_reviewed"])).days
        new_internals = dict(internals)
        new_internals["prior_day_count"] = days_since_review
        day_data_reviews[key] = new_internals
    return dict(sorted(day_data_reviews.items(), key=lambda x: x[1]["prior_day_count"], reverse=True))


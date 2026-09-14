from datetime import date
import json
from cards.grammar.grammar_cards import text_recall_grammar_g2e
from cards.syntax.syntax_cards import function_recall_syntax_g2e
from cards.card_utils import (
    review_card_sort_austin,
    card_instructions_loader,
    card_assembler_loader,
    format_review_item,
    card_llm_combination,
)
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


    def austin_form_initial_cards(self, new_items):
        pass



        # necessary variables - 
            # γράφω
            #     "key": "γράφω",
                # "part_of_speech": "verb",
                # "lexical_form": "γράφω",
                # "gloss": "I write",
                # "reference_card": {
                #     "card_type": "text_recall_vocabulary_g2e",
                #     "sentence": "ὁ ἄνθρωπος γράφει τὸν λόγον.",
                #     "translation": "The man writes the word.",
                #     "target_form": "γράφει"


    




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


    

    def austin_card_form_from_reviews(self):
        due_reviews = list(self.sort_vocabulary_by_due_date())
        relevant_review_cards = review_card_sort_austin(self=self, item_keys=due_reviews, domain_type="vocabulary")
        new_cards = []
        for review_key, card_type in zip(due_reviews, relevant_review_cards):
            item = self.vocabulary_scaffolding["items"][review_key]
            card_history = self.student_cards_by_item[review_key]["card_history"]
            instructions = card_instructions_loader(desired_card_type=card_type)
            formatted_item = format_review_item(item=item, card_history=card_history)
            llm_reply = card_llm_combination(llm_instructions=instructions, item=formatted_item)
            assembler = card_assembler_loader(desired_card_type=card_type)
            new_cards.append(assembler(item, llm_reply))
        return new_cards
                

        




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













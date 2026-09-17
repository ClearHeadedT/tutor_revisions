

def card_history_for_items(student_cards, due_reviews):
    """Returns a dict showing card history for each item of input 'due_reviews' keyed by mutual key.
    Items the student has met but never had a card for come back with an empty history."""
    return {key: student_cards.get(key, {}).get("card_history", []) for key in due_reviews}


def review_card_sort_austin(student_cards_by_item, item_keys, domain_type):
        """Sorts cards for me (Austin) in simple binary review session,
        text recall and cloze"""
        card_1 = None
        card_2 = None
        if domain_type == "grammar":
            card_1 = "text_recall_grammar_g2e"
            card_2 = "cloze_grammar_e2g"
        if domain_type == "vocabulary":
            card_1 = "text_recall_vocabulary_g2e"
            card_2 = "cloze_vocabulary_e2g"
        if domain_type == "syntax":
            card_1 = "function_recall_syntax_g2e"
            card_2 = "self_formulation_syntax_e2g"
        relevant_cards = []
        for key in item_keys:
            history = student_cards_by_item[key]["card_history"]
            current_item = history[-1]
            if (current_item["status_at_review"] == "learning"
                and current_item["correct"] == False
                and current_item["card_type"] == card_1):
                relevant_cards.append(card_1)
            elif (current_item["status_at_review"] == "learning"
                and current_item["correct"] == False
                and current_item["card_type"] == card_2
                and len(history) >= 2
                and history[-2]["correct"] == False):
                relevant_cards.append(card_1)
            else:
                relevant_cards.append(card_2)
        return relevant_cards
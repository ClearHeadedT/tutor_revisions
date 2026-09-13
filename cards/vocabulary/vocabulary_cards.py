from llm_calls.instructions import (
    GENERAL_CARD_INSTRUCTIONS,
    instructions_TextRecallVocabularyG2E,
    instructions_ClozeVocabularyE2G,
)
from cards.card_utils import card_llm_combination


def text_recall_vocabulary_g2e(item):
    """Student must correctly identify item in the context of a Gk sentence"""
    llm_instructions = GENERAL_CARD_INSTRUCTIONS + instructions_TextRecallVocabularyG2E
    student_instructions = "Identify the English translation of the following vocabulary item:\n\n"
    key = item["key"]
    formatted_review_item = f"'{key}'. Gloss: {item["gloss"]}"
    llm_call = card_llm_combination(llm_instructions=llm_instructions, formatted_item=formatted_review_item)
    front_of_card = student_instructions + llm_call + "\n\n" + key
    back_of_card = f"{item["lexical_form"]}: {item["gloss"]}"
    return (front_of_card, back_of_card)


def cloze_vocabulary_e2g(item):
    """Student is given a clozed out item in the context of a sentence and must identify item from English gloss"""
    llm_instructions = GENERAL_CARD_INSTRUCTIONS + instructions_ClozeVocabularyE2G
    student_instructions = "Identify the Greek lexical item missing in the following sentence:\n\n"
    key = next(iter(item))
    formatted_review_item = f"'{key}'. Gloss: {item["gloss"]}"
    llm_call = card_llm_combination(llm_instructions=llm_instructions, formatted_item=formatted_review_item)
    front_of_card = student_instructions + llm_call
    back_of_card = llm_call
    return (front_of_card, back_of_card)


def self_formulation_vocabulary_e2g(item):
    """Student must create a new sentence or phrase that uses the given Greek word."""
    student_instructions = f"Create a Koine Greek phrase or sentence for the following vocabulary word:\n\n"
    formatted_review_item = f"Gloss: {item["gloss"]}"
    front_of_card = student_instructions + formatted_review_item
    back_of_card = "Were you successful?"           # Eventually will need to implement LLM-based checking here 
    return (front_of_card, back_of_card)




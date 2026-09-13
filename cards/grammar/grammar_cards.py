from llm_calls.instructions import (
    GENERAL_CARD_INSTRUCTIONS,
    instructions_TextRecallGrammarG2E,
    instructions_RuleRecallGrammarG2E,
    instructions_ClozeGrammarE2G,
)
from cards.card_utils import card_llm_combination


def text_recall_grammar_g2e(item):
    """Student reads the sentence and must parse the target form"""
    llm_instructions = GENERAL_CARD_INSTRUCTIONS + instructions_TextRecallGrammarG2E
    student_instructions = "Parse the target form as it appears in the following sentence:\n\n"
    key = item["key"]
    formatted_review_item = f"'{key}'. Form: {item["form"]}. Parsing: {item["parsing"]}"
    llm_call = card_llm_combination(llm_instructions=llm_instructions, formatted_item=formatted_review_item)
    front_of_card = student_instructions + llm_call + "\n\n" + item["form"]
    back_of_card = f"{item["form"]}: {item["parsing"]}"
    return (front_of_card, back_of_card)


def rule_recall_grammar_g2e(item):
    """Student sees the form in context and must state its underlying rule of formation"""
    llm_instructions = GENERAL_CARD_INSTRUCTIONS + instructions_RuleRecallGrammarG2E
    student_instructions = "State the rule of formation for the target form in the following sentence:\n\n"
    key = item["key"]
    formatted_review_item = f"'{key}'. Form: {item["form"]}. Parsing: {item["parsing"]}"
    llm_call = card_llm_combination(llm_instructions=llm_instructions, formatted_item=formatted_review_item)
    front_of_card = student_instructions + llm_call + "\n\n" + item["form"]
    back_of_card = f"{item["form"]}: {item["rule"]}"
    return (front_of_card, back_of_card)


def cloze_grammar_e2g(item):
    """Student is given the parsing and lexical form and must produce the correctly inflected form"""
    llm_instructions = GENERAL_CARD_INSTRUCTIONS + instructions_ClozeGrammarE2G
    student_instructions = "Supply the correctly inflected Greek form missing in the following sentence:\n\n"
    key = item["key"]
    formatted_review_item = f"'{key}'. Form: {item["form"]}. Parsing: {item["parsing"]}. Lexical form: {item["lexical_form"]}"
    llm_call = card_llm_combination(llm_instructions=llm_instructions, formatted_item=formatted_review_item)
    front_of_card = student_instructions + llm_call + "\n\n" + f"{item["lexical_form"]}: {item["parsing"]}"
    back_of_card = f"{item["form"]}: {item["parsing"]}"
    return (front_of_card, back_of_card)

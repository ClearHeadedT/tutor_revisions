from ...llm_calls.instructions import (
    instructions_FunctionRecallSyntaxG2E,
    instructions_SelfFormulationSyntaxE2G,
    instructions_ValidityJudgmentSyntaxG2E,
)
from ..card_utils import card_llm_combination
import random


def function_recall_syntax_g2e(item):
    """Student sees the usage in a clause and states how it is functioning."""
    llm_instructions = instructions_FunctionRecallSyntaxG2E
    student_instructions = "Name the following syntactic usage and identify its basic force:\n"
    key = next(iter(item))
    formatted_review_item = f"'{key}'. Function: {item["description"]}"
    llm_call = card_llm_combination(llm_instructions=llm_instructions, formatted_item=formatted_review_item)
    front_of_card = student_instructions + llm_call
    back_of_card = formatted_review_item
    return (front_of_card, back_of_card)


def validity_judgment_syntax_g2e(item):
    """Student is given a syntactic category with hard contextual constraints for interpretation,
    (whether lexical, morphological contingency, or otherwise) and must state if the usage is valid or not."""
    llm_instructions = instructions_ValidityJudgmentSyntaxG2E
    student_instructions = (
        "The following syntactic category has a hard constraint, whether lexical, form requirements, or otherwise."
        "Identify what the constraint is, and if the following sentence is a VALID or INVALID syntactic usage accordingly:\n")
    positive_prompt = "Immediate task: write a VALID clause/short sentence according to the following hard constraints.:\n"
    negative_prompt = "Immediate task: write an INVALID and rule-violating clause or short sentence which violate the following hard constraints:\n"
    coin_flip = random.choice([1, 2])
    positive_or_negative = positive_prompt + item["hard_constraints"] if coin_flip == 1 else negative_prompt + item["hard_constraints"]
    key = next(iter(item))
    formatted_review_item = f"'{key}'\n Function: {item["description"]}\n {positive_or_negative}"
    llm_call = card_llm_combination(llm_instructions=llm_instructions, formatted_item=formatted_review_item)
    front_of_card = student_instructions + llm_call
    back_of_card = f"{key}: {item["description"]}\n Hard constraints: {item["hard_constraints"]}"
    return (front_of_card, back_of_card)


def self_formulation_syntax_e2g(item):
    """Student must create a new sentence or phrase that utilizes the given syntactic category, Greek lexical item, and sentence cue."""
    llm_instructions = instructions_SelfFormulationSyntaxE2G
    student_instructions = (
        "Create a Koine Greek phrase or sentence for the following syntactic category.\n"
        "Utilize the syntactic category to modify the provided lemma under the given scenario:\n")
    key = next(iter(item))
    formatted_review_item = f"'{key}'\n Function: {item["description"]}\n Lexeme options: {item["lexical_options"]}"
    llm_call = card_llm_combination(llm_instructions=llm_instructions, formatted_item=formatted_review_item)
    llm_split = llm_call.split("\n\n")
    front_of_card = student_instructions + llm_split[0]
    back_of_card = f"{key}: {item["description"]}\n Example solutions: {llm_split[1]}"
    return (front_of_card, back_of_card)




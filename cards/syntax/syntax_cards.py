import random


def function_recall_syntax_g2e(item, llm_reply):
    """Student sees the usage in a clause and states how it is functioning."""
    student_instructions = "Name the following syntactic usage and identify its basic force:\n"
    front_of_card = student_instructions + llm_reply["sentence"]
    back_of_card = f"{item["key"]}: {item["description"]}"
    return (front_of_card, back_of_card)


def validity_judgment_prompt(item):
    """Decides which way this card is asked before the LLM call, since the model needs
    telling whether to write a valid usage or to breach one constraint. Roughly half
    come out each way, which is what keeps the student judging rather than guessing."""
    positive_prompt = "Immediate task: write a VALID clause/short sentence according to the following hard constraints.:\n"
    negative_prompt = "Immediate task: write an INVALID and rule-violating clause or short sentence which violate the following hard constraints:\n"
    hard_constraints = "\n".join(item["hard_constraints"])
    coin_flip = random.choice([1, 2])
    return positive_prompt + hard_constraints if coin_flip == 1 else negative_prompt + hard_constraints


def validity_judgment_syntax_g2e(item, llm_reply):
    """Student is given a syntactic category with hard contextual constraints for interpretation,
    (whether lexical, morphological contingency, or otherwise) and must state if the usage is valid or not."""
    student_instructions = (
        "The following syntactic category has a hard constraint, whether lexical, form requirements, or otherwise."
        "Identify what the constraint is, and if the following sentence is a VALID or INVALID syntactic usage accordingly:\n")
    hard_constraints = "\n".join(item["hard_constraints"])
    front_of_card = student_instructions + llm_reply["sentence"]
    back_of_card = f"{item["key"]}: {item["description"]}\n Hard constraints: {hard_constraints}"
    return (front_of_card, back_of_card)


def self_formulation_syntax_e2g(item, llm_reply):
    """Student must create a new sentence or phrase that utilizes the given syntactic category, Greek lexical item, and sentence cue."""
    student_instructions = (
        "Create a Koine Greek phrase or sentence for the following syntactic category.\n"
        "Utilize the syntactic category to modify the provided lemma under the given scenario:\n")
    front_of_card = student_instructions + llm_reply["translation"]
    back_of_card = f"{item["key"]}: {item["description"]}\n Example solution: {llm_reply["sentence"]}"
    return (front_of_card, back_of_card)

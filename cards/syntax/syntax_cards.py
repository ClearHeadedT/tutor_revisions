import random


def function_recall_syntax_g2e(item, llm_reply):
    """Student sees the usage in a clause and states how it is functioning."""
    student_instructions = "Name the following syntactic usage and identify its basic force:\n"
    front_of_card = student_instructions + llm_reply["sentence"]
    back_of_card = f"{item["display_name"]}: {item["description"]}"
    return (front_of_card, back_of_card)


def validity_judgment_prompt():
    """Decides which way this card is asked before the LLM call, since the model needs
    telling whether to write a sound usage or to breach one of the conditions the usage
    requires. Roughly half come out each way, which is what keeps the student judging
    rather than guessing."""
    valid = "Immediate task: write a VALID clause or short sentence, one meeting every condition this usage requires.\n"
    invalid = "Immediate task: write an INVALID clause or short sentence, one breaching exactly one condition this usage requires.\n"
    return random.choice([valid, invalid])


def validity_judgment_syntax_g2e(item, llm_reply):
    """Student is given a syntactic usage whose definition carries conditions, whether
    lexical, morphological or otherwise, and must state if the usage is valid or not."""
    student_instructions = (
        "The following syntactic usage carries conditions, whether lexical, morphological, or otherwise. "
        "Identify what they are, and say whether the sentence below is a VALID or INVALID use accordingly:\n")
    front_of_card = student_instructions + llm_reply["sentence"]
    back_of_card = f"{item["display_name"]}: {item["description"]}"
    return (front_of_card, back_of_card)


def self_formulation_syntax_e2g(item, llm_reply):
    """Student must create a new sentence or phrase exhibiting the given syntactic usage,
    working from an English cue."""
    student_instructions = (
        "Create a Koine Greek phrase or sentence exhibiting the following syntactic usage,\n"
        "rendering the scenario below:\n")
    front_of_card = student_instructions + llm_reply["translation"]
    back_of_card = f"{item["display_name"]}: {item["description"]}\n Example solution: {llm_reply["sentence"]}"
    return (front_of_card, back_of_card)

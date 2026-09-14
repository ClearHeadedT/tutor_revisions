def assemble_text_recall_vocabulary_g2e(item, llm_reply):
    """Student must correctly identify item in the context of a Gk sentence"""
    student_instructions = "Identify the English translation of the following vocabulary item:\n\n"
    front_of_card = student_instructions + llm_reply + "\n\n" + item["key"]
    back_of_card = f"{item["lexical_form"]}: {item["gloss"]}"
    return (front_of_card, back_of_card)


def assemble_cloze_vocabulary_e2g(item, llm_reply):
    """Student is given a clozed out item in the context of a sentence and must identify item from English gloss"""
    student_instructions = "Identify the Greek lexical item missing in the following sentence:\n\n"
    front_of_card = student_instructions + llm_reply
    back_of_card = llm_reply
    return (front_of_card, back_of_card)


def self_formulation_vocabulary_e2g(item):
    """Student must create a new sentence or phrase that uses the given Greek word."""
    student_instructions = f"Create a Koine Greek phrase or sentence for the following vocabulary word:\n\n"
    formatted_review_item = f"Gloss: {item["gloss"]}"
    front_of_card = student_instructions + formatted_review_item
    back_of_card = "Were you successful?"           # Eventually will need to implement LLM-based checking here
    return (front_of_card, back_of_card)



def assemble_text_recall_vocabulary_g2e(item, llm_reply):
    """Student must correctly identify item in the context of a Gk sentence"""
    instructions_for_student = "Identify the English translation of the following vocabulary item:\n\n"
    front_of_card = instructions_for_student + llm_reply["sentence"] + "\n\n" + llm_reply["target_form"]
    back_of_card = f"{item["lexical_entry"]}: {item["gloss"]}"
    return (front_of_card, back_of_card)


def assemble_cloze_vocabulary_e2g(item, llm_reply):
    """Student is given a clozed out item in the context of a sentence and must identify item from English gloss"""
    instructions_for_student = "Identify the Greek lexical item missing in the following sentence:\n\n"
    clozed_sentence = llm_reply["sentence"].replace(llm_reply["target_form"], "_____")
    front_of_card = instructions_for_student + clozed_sentence + "\n\n" + llm_reply["translation"]
    back_of_card = f"{llm_reply["target_form"]} ({item["lexical_entry"]}: {item["gloss"]})"
    return (front_of_card, back_of_card)


def self_formulation_vocabulary_e2g(item):
    """Student must create a new sentence or phrase that uses the given Greek word."""
    instructions_for_student = f"Create a Koine Greek phrase or sentence for the following vocabulary word:\n\n"
    formatted_review_item = f"Gloss: {item["gloss"]}"
    front_of_card = instructions_for_student + formatted_review_item
    back_of_card = "Were you successful?"           # Eventually will need to implement LLM-based checking here
    return (front_of_card, back_of_card)

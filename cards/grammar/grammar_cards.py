
def text_recall_grammar_g2e(item, llm_reply):
    """Student reads the sentence and must parse the target form"""
    student_instructions = "Parse the target form as it appears in the following sentence:\n\n"
    front_of_card = student_instructions + llm_reply["sentence"] + "\n\n" + llm_reply["target_form"]
    back_of_card = f"{item["form"]}: {item["parsing"]}"
    return (front_of_card, back_of_card)


def rule_recall_grammar_g2e(item, llm_reply):
    """Student sees the form in context and must state its underlying rule of formation"""
    student_instructions = "State the rule of formation for the target form in the following sentence:\n\n"
    front_of_card = student_instructions + llm_reply["sentence"] + "\n\n" + llm_reply["target_form"]
    back_of_card = f"{item["form"]}: {item["rule"]}"
    return (front_of_card, back_of_card)


def cloze_grammar_e2g(item, llm_reply):
    """Student is given the parsing and lexical form and must produce the correctly inflected form"""
    student_instructions = "Supply the correctly inflected Greek form missing in the following sentence:\n\n"
    front_of_card = student_instructions + llm_reply["sentence"] + "\n\n" + f"{item["lexical_form"]}: {item["parsing"]}"
    back_of_card = f"{item["form"]}: {item["parsing"]}"
    return (front_of_card, back_of_card)

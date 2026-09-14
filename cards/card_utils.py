import json

from llm_calls.llm_constants import MAX_TOKENS, CARD_MODEL
from llm_calls.client import make_client
from llm_calls.instructions import (
    GENERAL_CARD_INSTRUCTIONS,
    instructions_TextRecallGrammarG2E,
    instructions_ClozeGrammarE2G,
    instructions_TextRecallVocabularyG2E,
    instructions_ClozeVocabularyE2G,
    instructions_FunctionRecallSyntaxG2E,
    instructions_SelfFormulationSyntaxE2G
)
from cards.vocabulary.vocabulary_cards import (
    assemble_text_recall_vocabulary_g2e,
    assemble_cloze_vocabulary_e2g,
)

def format_review_item(item, card_history):
    """The user message. The item object already holds everything relevant to its
    domain, so it goes over as JSON rather than being retyped into a sentence."""
    return json.dumps(
        {"item": item, "recent_generations": card_history[-3:]},
        indent=2,
        ensure_ascii=False,
    )


def card_llm_combination(llm_instructions, item):
    client = make_client()
    response = client.messages.create(
        model=CARD_MODEL,
        max_tokens=MAX_TOKENS,
        system=llm_instructions,
        messages=[{"role": "user", "content": item}],
    )
    return response.content[0].text

def card_instructions_loader(desired_card_type):
    instructions = None
    match desired_card_type:
        case "text_recall_grammar_g2e":
            instructions = GENERAL_CARD_INSTRUCTIONS + instructions_TextRecallGrammarG2E
        case "cloze_grammar_e2g":
            instructions = GENERAL_CARD_INSTRUCTIONS + instructions_ClozeGrammarE2G
        case "text_recall_vocabulary_g2e":
            instructions = GENERAL_CARD_INSTRUCTIONS + instructions_TextRecallVocabularyG2E
        case "cloze_vocabulary_e2g":
            instructions = GENERAL_CARD_INSTRUCTIONS + instructions_ClozeVocabularyE2G
        case "function_recall_syntax_g2e":
            instructions = instructions_FunctionRecallSyntaxG2E
        case "self_formulation_syntax_e2g":
            instructions = instructions_SelfFormulationSyntaxE2G
    return instructions

def card_assembler_loader(desired_card_type):
    assembler = None
    match desired_card_type:
        case "text_recall_vocabulary_g2e":
            assembler = assemble_text_recall_vocabulary_g2e
        case "cloze_vocabulary_e2g":
            assembler = assemble_cloze_vocabulary_e2g
    return assembler


def review_card_sort_austin(self, item_keys, domain_type):
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
            history = self.student_cards_by_item[key]["card_history"]
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





# need cards paired to their respective difficulties based on JSON student vocabulary data 

    
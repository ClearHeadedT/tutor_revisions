import json

from greek_text import normalize_greek
from data.student_data.student_data_helper_functions import (
    load_vocabulary_senses,
    save_vocabulary_senses,
)
from llm_calls.instructions import (
    GENERAL_CARD_INSTRUCTIONS,
    instructions_TextRecallGrammarG2E,
    instructions_ClozeGrammarE2G,
    instructions_TextRecallVocabularyG2E,
    instructions_ClozeVocabularyE2G,
    instructions_FunctionRecallSyntaxG2E,
    instructions_SelfFormulationSyntaxE2G
)






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


def cache_vocabulary_senses(lexemes):
    """Enriches any of these words the cache does not already hold and writes them back.
    This is the only path that touches Text-Fabric -- it costs ~4 seconds and 2.2 GB to
    open the dataset, so it is run deliberately for a batch rather than per card.

    lexemes are (form, lexical_entry) pairs, the same shape the card class takes."""
    from text_fabric.main import word_enrichment_batch

    senses = load_vocabulary_senses()
    missing = {normalize_greek(form): entry for form, entry in lexemes
               if normalize_greek(form) not in senses}
    if not missing:
        return senses
    for lemma, enrichment in word_enrichment_batch(missing).items():
        if enrichment is None:
            raise ValueError(f"{lemma} has no occurrences in the GNT")
        senses[lemma] = {"lexical_entry": missing[lemma], **enrichment}
    save_vocabulary_senses(senses)
    return senses


def parse_card_reply(llm_reply):
    """OUTPUT FORMAT tells the model to wrap its JSON object in a ```json fence,
    so the fence comes off before the card can be stored as an object."""
    fenced = llm_reply.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    return json.loads(fenced)


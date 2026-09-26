import json
import re

from greek_text import normalize_greek
from data.student_data.student_data_helper_functions import (
    load_vocabulary_senses,
    save_vocabulary_senses,
    load_grammar_scaffolding,
    load_syntax_scaffolding,
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
            instructions = GENERAL_CARD_INSTRUCTIONS + instructions_FunctionRecallSyntaxG2E
        case "self_formulation_syntax_e2g":
            instructions = GENERAL_CARD_INSTRUCTIONS + instructions_SelfFormulationSyntaxE2G
    return instructions


def enrich_vocabulary_senses(lexemes):
    """Enriches words from Text-Fabric and Louw-Nida and stores the result under its
    lemma. Words already stored are passed over, since their enrichment cannot change.
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



def unpack_grammatical_item(grammar_item_key):
    """Parses out a grammatical object from the JSON in a coherent format 
    for card-creation LLM digestion"""
    grammar_scaffolding = load_grammar_scaffolding()
    item = grammar_scaffolding["items"][grammar_item_key]
    rule = grammar_scaffolding["structure"][item["rule"]]
    return {"item": item, "rule": without_patterns(rule), "pattern": rule["patterns"][item["parent"]]}


def without_patterns(rule):
    """A rule's own fields. Its patterns list every item under it, most of which the card is not about."""
    return {field: value for field, value in rule.items() if field != "patterns"}




def unpack_syntactic_item(syntax_item_key):
    """The usage itself, the categories it sits under, and the neighbouring usages a
    clause has to exclude -- the syntax counterpart of a grammar item's rule and paradigm.

    Keys are paths and the scaffolding nests under whole keys, so the prefixes of the key
    are the child keys at each level and the walk down is a lookup per segment."""
    structure = load_syntax_scaffolding()["structure"]
    segments = syntax_item_key.split("/")
    chain, level = [], structure
    for depth in range(len(segments)):
        node = level["/".join(segments[:depth + 1])]
        chain.append(node)
        level = node.get("children", {})
    siblings = chain[-2].get("children", {}) if len(chain) > 1 else structure
    return {
        "item": {"key": syntax_item_key, **without_children(chain[-1])},
        "ancestors": [without_pairings(node) for node in chain[:-1]],
        "sibling_usages": {key: without_pairings(node) for key, node in siblings.items()
                           if key != syntax_item_key},
    }


def without_children(node):
    """A scaffolding node's own fields. The children carry whole subtrees, which would
    swamp the prompt with material the card is not about."""
    return {field: value for field, value in node.items() if field != "children"}


def without_pairings(node):
    """A usage the card is not about. Its GNT pairings are for its own cards; this card is
    held to the item's."""
    return {field: value for field, value in node.items() if field not in ("children", "gnt_lexemes")}


def parse_card_reply(llm_reply):
    """OUTPUT FORMAT tells the model to wrap its JSON object in a ```json fence. The object is taken
    from inside the fence, or failing that from the first brace to the last, so a reply that wraps
    the fence in a sentence of prose is still read."""
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", llm_reply, re.DOTALL)
    if fenced:
        return json.loads(fenced.group(1))
    start, end = llm_reply.find("{"), llm_reply.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object in the reply")
    return json.loads(llm_reply[start:end + 1])

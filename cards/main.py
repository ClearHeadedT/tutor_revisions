from cards.vocabulary.vocabulary_cards import (
    assemble_text_recall_vocabulary_g2e,
    assemble_cloze_vocabulary_e2g,
)
from cards.grammar.grammar_cards import (
    text_recall_grammar_g2e,
    rule_recall_grammar_g2e,
    cloze_grammar_e2g,
)
from cards.syntax.syntax_cards import (
    function_recall_syntax_g2e,
    validity_judgment_syntax_g2e,
    self_formulation_syntax_e2g,
)


def card_assembler_loader(desired_card_type):
    """Picks the assembler for a card type. Every assembler takes (item, llm_reply)
    and returns a (front, back) pair, so a caller holding both can render any type
    without knowing which one it has."""
    assembler = None
    match desired_card_type:
        case "text_recall_vocabulary_g2e":
            assembler = assemble_text_recall_vocabulary_g2e
        case "cloze_vocabulary_e2g":
            assembler = assemble_cloze_vocabulary_e2g
        case "text_recall_grammar_g2e":
            assembler = text_recall_grammar_g2e
        case "rule_recall_grammar_g2e":
            assembler = rule_recall_grammar_g2e
        case "cloze_grammar_e2g":
            assembler = cloze_grammar_e2g
        case "function_recall_syntax_g2e":
            assembler = function_recall_syntax_g2e
        case "validity_judgment_syntax_g2e":
            assembler = validity_judgment_syntax_g2e
        case "self_formulation_syntax_e2g":
            assembler = self_formulation_syntax_e2g
    return assembler

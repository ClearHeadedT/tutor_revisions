from tasks.new_card_creation.new_card import NewVocabularyCard, NewGrammarCard, NewSyntaxCard


def create_new_vocabulary_cards(lexemes, student, desired_card_type):
    """Makes one card per word at the student's level and records each to their history.

    lexemes are (form, lexical_entry) pairs -- the plain form Text-Fabric indexes, and
    the conventional lexicon form carrying the article and gender."""
    new_cards = {}
    for lexeme in lexemes:
        card_class = NewVocabularyCard(lexeme, student)
        card = card_class.generate_vocabulary_card(desired_card_type)
        student.record_card(key=card_class.lemma, card=card, domain="vocabulary")
        new_cards[card_class.lemma] = card
    return new_cards


def create_new_grammar_cards(grammar_item_keys, student, desired_card_type):
    """Makes one card per grammar slot at the student's level and records each to their
    history.

    grammar_item_keys are slot keys from the grammar scaffolding, such as
    decl2::n-2a::genitive.singular."""
    new_cards = {}
    for key in grammar_item_keys:
        card_class = NewGrammarCard(key, student)
        card = card_class.generate_grammar_card(desired_card_type)
        student.record_card(key=key, card=card, domain="grammar")
        new_cards[key] = card
    return new_cards


def create_new_syntax_cards(syntax_item_keys, student, desired_card_type):
    """Makes one card per syntactic usage at the student's level and records each to their
    history.

    syntax_item_keys are paths into the syntax scaffolding, such as
    dative/pure-dative-uses/dative-indirect-object."""
    new_cards = {}
    for key in syntax_item_keys:
        card_class = NewSyntaxCard(key, student)
        card = card_class.generate_syntax_card(desired_card_type)
        student.record_card(key=key, card=card, domain="syntax")
        new_cards[key] = card
    return new_cards

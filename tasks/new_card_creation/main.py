from datetime import date

from tasks.new_card_creation.new_card import NewVocabularyCard
from tasks.new_card_creation.utils import cache_vocabulary_senses
from greek_text import normalize_greek


def create_new_vocabulary_cards(lexemes, student, desired_card_type):
    """Introduces a batch of words to a student: enriches whatever the shared cache is
    missing, generates one reference card per word at the student's level, and records
    each word as learning with its card.

    lexemes are (form, lexical_entry) pairs -- the plain form Text-Fabric indexes, and
    the conventional lexicon form carrying the article and gender."""
    senses = cache_vocabulary_senses(lexemes)
    student_overview = student.student_overview()
    today = date.today().isoformat()
    new_cards = {}
    for form, _ in lexemes:
        lemma = normalize_greek(form)
        card_class = NewVocabularyCard(lemma=lemma, senses=senses)
        card = card_class.generate_vocabulary_card(
            desired_card_type=desired_card_type,
            student_overview=student_overview,
        )
        student.record_card(lemma=lemma, card=card, today=today)
        new_cards[lemma] = card
    return new_cards

from datetime import date

from tasks.initial_card_creation.new_card import NewVocabularyCard
from tasks.initial_card_creation.utils import cache_vocabulary_senses
from greek_text import normalize_greek


def create_new_cards(lexemes, student, desired_card_type="text_recall_vocabulary_g2e"):
    """Introduces a batch of words to a student: enriches whatever the shared cache is
    missing, generates one reference card per word at the student's level, and records
    each word as learning with its card.

    lexemes are (form, lexical_entry) pairs -- the plain form Text-Fabric indexes, and
    the conventional lexicon form carrying the article and gender."""
    unseen = [pair for pair in lexemes if normalize_greek(pair[0]) not in student.vocabulary]
    senses = cache_vocabulary_senses(unseen)
    student_overview = student.student_overview()
    today = date.today().isoformat()
    new_cards = {}
    for form, _ in unseen:
        lemma = normalize_greek(form)
        card_class = NewVocabularyCard(lemma=lemma, senses=senses)
        reference_card = card_class.generate_vocabulary_card(
            desired_card_type=desired_card_type,
            student_overview=student_overview,
        )
        student.record_new_vocabulary(lemma=lemma, reference_card=reference_card, first_seen=today)
        new_cards[lemma] = reference_card
    return new_cards

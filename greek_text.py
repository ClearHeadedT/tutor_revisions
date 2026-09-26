import re
import unicodedata


def normalize_greek(text):
    """Koine lemmas appear in two Unicode blocks whose accented vowels render
    identically but compare unequal. NFC collapses them, so Greek used as a
    dict key must pass through here wherever it enters the system."""
    return unicodedata.normalize("NFC", text)


def fold_greek(text):
    """Greek with accents, breathings and case removed, and final sigma made medial. Two
    spellings of one word fold to the same string, which is what a comparison against the
    corpus needs - a card that moves an accent or capitalises a word has not changed its words."""
    stripped = "".join(c for c in unicodedata.normalize("NFD", text)
                       if unicodedata.category(c) != "Mn")
    return unicodedata.normalize("NFC", stripped.lower().replace("ς", "σ"))


GREEK_WORD = re.compile(r"[Ͱ-Ͽἀ-῿]+")


def greek_tokens(text):
    """The Greek words in a string, folded, in order. Punctuation, cloze braces and anything
    that is not Greek fall away."""
    return [fold_greek(word) for word in GREEK_WORD.findall(text)]


def greek_words(text):
    """The Greek words in a string as written - accents kept - in order."""
    return [normalize_greek(word) for word in GREEK_WORD.findall(normalize_greek(text))]

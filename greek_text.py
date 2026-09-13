import unicodedata


def normalize_greek(text):
    """Koine lemmas appear in two Unicode blocks whose accented vowels render
    identically but compare unequal. NFC collapses them, so Greek used as a
    dict key must pass through here wherever it enters the system."""
    return unicodedata.normalize("NFC", text)

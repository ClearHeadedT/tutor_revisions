"""A verb's principal parts and government as the GNT attests them, handed over with a vocabulary item.

The sentence plan's charts are built on paradigm verbs; a word's own stems are what a model most
often gets wrong, and the grammars' charts cannot supply them - εἶπαν, ἔγνων and ἐλήλυθα follow
from the word, not the paradigm. So a verb item carries one attested form for each principal part,
the case its objects take, and the prepositions it is commonly used with. Nouns and adjectives
carry nothing extra: their lexical entry already gives gender and declension. Forms only, never the
verses they come from. Read from corpus_index.json, so Text-Fabric is never opened here.
"""

from greek_text import fold_greek
from tasks.new_card_creation.verify import LEMMA_ALIASES, verb_forms
from text_fabric.corpus_index import load_corpus_index

NOT_ATTESTED = "not attested in the GNT"
PREPOSITIONS = 3
# An object case or preposition met once is as likely an oddity of one clause as a habit of the verb.
MIN_OCCURRENCES = 2

# (principal part, tense, the voices that can stand for it in preference order). A deponent's
# present and future are middle, so those parts take whichever voice the verb has.
PRINCIPAL_PARTS = [
    ("present", "present", ("active", "middle/passive", "middle", "passive")),
    ("future", "future", ("active", "middle")),
    ("aorist", "aorist", ("active", "middle")),
    ("perfect active", "perfect", ("active",)),
    ("perfect middle/passive", "perfect", ("middle/passive", "middle", "passive")),
    ("aorist passive", "aorist", ("passive",)),
]


def _principal_part(forms, tense, voices):
    """One attested form for a principal part: its commonest indicative, otherwise its commonest
    form in any mood. The commonest rather than the first singular, which the corpus may attest
    only in a rare variant (ἐκέκραξα beside ἔκραξεν)."""
    for voice in voices:
        candidates = [f for f in forms if f[1] == tense and f[2] == voice]
        if not candidates:
            continue
        indicative = [f for f in candidates if f[3] == "indicative"]
        form = max(indicative or candidates, key=lambda f: f[5])
        return f"{form[0]} ({form[4]})"
    return NOT_ATTESTED


def lexical_profile(lemma):
    """A verb's principal parts, object case and prepositions; None for anything but a verb."""
    forms = verb_forms().get(LEMMA_ALIASES.get(fold_greek(lemma), fold_greek(lemma)))
    if not forms:
        return None
    profile = {"principal_parts": {part: _principal_part(forms, tense, voices)
                                   for part, tense, voices in PRINCIPAL_PARTS}}
    frame = next((frame for verb, frame in load_corpus_index()["frames"].items()
                  if fold_greek(verb) == fold_greek(lemma)), {})
    objects = {case: n for case, n in (frame.get("objects") or {}).items() if n >= MIN_OCCURRENCES}
    profile["object_case"] = (", ".join(f"{case} (x{count})" for case, count in objects.items())
                              if objects else "no object attested in the GNT")
    prepositions = [(prep, n) for prep, n in (frame.get("prepositions") or {}).items()
                    if n >= MIN_OCCURRENCES][:PREPOSITIONS]
    profile["prepositions"] = ([f"{prep} (x{count})" for prep, count in prepositions]
                               if prepositions else NOT_ATTESTED)
    return profile

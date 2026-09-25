"""Builds vocabulary_scaffolding.json from Text-Fabric: every GNT lemma at MIN_VOCAB occurrences
or more.

One corpus pass, which is the expensive part - loading N1904 costs about nine seconds, so
everything that needs the corpus happens inside `build()`.

This used to build card_randomizer_elements.json as well, pools of verbs and the subjects and
objects drawn against them. Those are gone: the pairs came out 2-10% attested with their verb, and
the sentence plan now leaves the choice of words to the model (see card_randomize_utils).

Two things worth knowing before editing:

**Text-Fabric is the right source here and the wrong source for paradigms.** It carries exact
frequency, part of speech, Louw-Nida domain and syntactic role for every word in the corpus. It
does not carry complete paradigms: only 18 verbs attest all six present active indicative forms
and exactly one attests all six imperfect active indicative. Teaching paradigms come from the
recovered charts instead - see derive_grammar_data.py.

**A lemma's natural frame is the slot it actually occupies.** pistis is overwhelmingly an
adverbial dative (instrumental), onoma likewise, anthropos a nominative subject. A review item
placed in its own frame reads like Greek; one assigned a slot at random often does not. `role`
is present on only 36% of words, so 17% of the pool has no frame and gets none rather than a
guessed one.
"""

import collections
import json
from pathlib import Path

from greek_text import normalize_greek
from text_fabric.fabric_utils import load_n1904

DATA = Path("data/curriculum_data")
VOCABULARY_PATH = DATA / "vocabulary_scaffolding.json"

# Occurrence floor for the vocabulary.
MIN_VOCAB = 10

# TF's part-of-speech tags, mapped onto the names the curriculum already uses.
POS_NAMES = {
    "subs": "noun", "verb": "verb", "adjv": "adjective", "advb": "adverb",
    "art": "article", "conj": "conjunction", "intj": "interjection",
    "num": "numeral", "prep": "preposition", "pron": "pronoun",
}
# How many (role, case) pairs to keep as a lemma's natural frame.
FRAME_DEPTH = 3


def _domain(api, node):
    """The Louw-Nida domain number on a word, or None. `ln` reads '33.100'; a few words carry
    several senses separated by spaces, and the first is the one tagged for this occurrence."""
    senses = (api.F.ln.v(node) or "").split()
    return senses[0].split(".")[0] if senses else None


def _majority(values):
    counted = collections.Counter(v for v in values if v)
    return counted.most_common(1)[0][0] if counted else None


def _in_prepositional_phrase(api, node):
    phrase = api.L.u(node, otype="phrase")
    return bool(phrase) and any(
        api.F.sp.v(w) == "prep" for w in api.L.d(phrase[0], otype="word"))


def _natural_frame(api, nodes):
    """The (role, case) slots this lemma actually occupies, commonest first.

    Reported with counts rather than as a single winner, so a consumer can see whether a frame
    rests on thirty occurrences or one."""
    slots = collections.Counter()
    for node in nodes:
        role = api.F.role.v(node)
        if not role:
            continue
        where = "prep-object" if _in_prepositional_phrase(api, node) else role
        slots[(where, api.F.case.v(node))] += 1
    return [{"role": role, "case": case, "occurrences": count}
            for (role, case), count in slots.most_common(FRAME_DEPTH)]


def _index_corpus(api):
    """Every word node grouped by normalized lemma, in one pass."""
    index = collections.defaultdict(list)
    for node in api.F.otype.s("word"):
        index[normalize_greek(api.F.lemma.v(node) or "")].append(node)
    index.pop("", None)
    return index


def build():
    api = load_n1904().api
    corpus = _index_corpus(api)

    part_of_speech, domains, glosses = {}, {}, {}
    for lemma, nodes in corpus.items():
        part_of_speech[lemma] = POS_NAMES.get(_majority(api.F.sp.v(n) for n in nodes), "other")
        domains[lemma] = _majority(_domain(api, n) for n in nodes)
        attested = [api.F.gloss.v(n) for n in nodes if api.F.gloss.v(n)]
        glosses[lemma] = max(attested, key=len) if attested else None

    vocabulary = {}
    for lemma, nodes in sorted(corpus.items(), key=lambda kv: -len(kv[1])):
        if len(nodes) < MIN_VOCAB:
            continue
        entry = {
            "key": lemma,
            "part_of_speech": part_of_speech[lemma],
            "lexical_form": lemma,
            "gloss": glosses[lemma],
            "frequency": len(nodes),
            "domain": domains[lemma],
        }
        frame = _natural_frame(api, nodes)
        if frame:
            entry["natural_frame"] = frame
        if part_of_speech[lemma] == "noun":
            entry["gender"] = _majority(api.F.gender.v(n) for n in nodes)
            entry["proper"] = _majority(api.F.typems.v(n) for n in nodes) == "proper"
        vocabulary[lemma] = entry

    return vocabulary


def write():
    vocabulary = build()

    existing = json.loads(VOCABULARY_PATH.read_text(encoding="utf-8"))
    # Hand-written fields on the seed entries - reference_card and the like - are kept. The
    # derivation owns frequency, domain and frame; it does not own what someone wrote by hand.
    for lemma, entry in existing.get("items", {}).items():
        if lemma in vocabulary:
            vocabulary[lemma] = {**entry, **vocabulary[lemma]}
        else:
            vocabulary[lemma] = entry

    structure = collections.defaultdict(list)
    for lemma, entry in vocabulary.items():
        structure[entry["part_of_speech"]].append(lemma)
    payload = {
        "source": {"corpus": "CenterBLC/N1904", "floor": MIN_VOCAB,
                   "note": "Frequency, part of speech, domain, gloss and natural frame are "
                           "derived from the corpus; anything else on an item is hand-written."},
        "structure": {name: {"name": name.title() + "s", "sequence": index + 1,
                             "items": sorted(lemmas)}
                      for index, (name, lemmas) in enumerate(sorted(structure.items()))},
        "items": vocabulary,
    }
    VOCABULARY_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    return len(vocabulary)


if __name__ == "__main__":
    print("vocabulary %d" % write())

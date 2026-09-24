"""Builds the two lexical JSONs from Text-Fabric.

    vocabulary_scaffolding.json   every GNT lemma at MIN_VOCAB occurrences or more
    card_randomizer_elements.json the verb and substantive pools the randomizer draws from

Both come from one corpus pass, which is the expensive part - loading N1904 costs about nine
seconds, so everything that needs the corpus happens inside `build()`.

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
ELEMENTS_PATH = DATA / "card_randomizer_elements.json"

# Occurrence floors. The verb pool is tighter because a verb anchors a whole sentence and needs
# enough attested forms to be usable in several constructions; a substantive only has to fill
# one slot.
MIN_VOCAB = 10
MIN_VERB = 20

# TF's part-of-speech tags, mapped onto the names the curriculum already uses.
POS_NAMES = {
    "subs": "noun", "verb": "verb", "adjv": "adjective", "advb": "adverb",
    "art": "article", "conj": "conjunction", "intj": "interjection",
    "num": "numeral", "prep": "preposition", "pron": "pronoun",
}
# How many (role, case) pairs to keep as a lemma's natural frame.
FRAME_DEPTH = 3
# A verb's object case is called settled when this much of its attested objects agree.
GOVERNMENT_CONFIDENT = 0.7


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


def _arguments_by_verb(api):
    """Which lemmas and which domains each verb actually takes as subject and object.

    Only clauses holding exactly one verb are counted. A clause with two verbs cannot say which
    of them an object belongs to without walking the dependency edges, and a wrong pairing is
    worse here than a missing one."""
    lemma_pairs = {"s": collections.defaultdict(collections.Counter),
                   "o": collections.defaultdict(collections.Counter)}
    domain_pairs = {"s": collections.defaultdict(collections.Counter),
                    "o": collections.defaultdict(collections.Counter)}
    object_cases = collections.defaultdict(collections.Counter)
    prepositions = collections.defaultdict(collections.Counter)

    for node in api.F.otype.s("word"):
        clause = api.L.u(node, otype="clause")
        if not clause:
            continue
        verbs = [w for w in api.L.d(clause[0], otype="word") if api.F.sp.v(w) == "verb"]
        if len(verbs) != 1:
            continue
        verb = normalize_greek(api.F.lemma.v(verbs[0]) or "")

        if api.F.sp.v(node) == "prep":
            prepositions[verb][normalize_greek(api.F.lemma.v(node) or "")] += 1
            continue

        role = api.F.role.v(node)
        if role in ("o", "o2") and api.F.case.v(node):
            object_cases[verb][api.F.case.v(node)] += 1
        if role not in ("s", "o") or api.F.sp.v(node) != "subs":
            continue
        lemma_pairs[role][verb][normalize_greek(api.F.lemma.v(node) or "")] += 1
        verb_domain, argument_domain = _domain(api, verbs[0]), _domain(api, node)
        if verb_domain and argument_domain:
            domain_pairs[role][verb_domain][argument_domain] += 1

    return lemma_pairs, domain_pairs, object_cases, prepositions


def _government(cases):
    """A verb's object case, with how strongly the corpus agrees.

    akouo takes 63 accusatives and 45 genitives, which is not a rule but a real split the
    grammars also report; calling it 'accusative' outright would be false. `confidence` is what
    lets a caller prefer the verbs that behave consistently."""
    if not cases:
        return {"case": None, "confidence": 0.0, "attested": {}}
    total = sum(cases.values())
    case, count = cases.most_common(1)[0]
    return {"case": case, "confidence": round(count / total, 2), "attested": dict(cases)}


def build():
    api = load_n1904().api
    corpus = _index_corpus(api)
    lemma_pairs, domain_pairs, object_cases, prepositions = _arguments_by_verb(api)

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

    nouns_by_domain = collections.defaultdict(list)
    for lemma, entry in vocabulary.items():
        if entry["part_of_speech"] == "noun" and entry["domain"]:
            nouns_by_domain[entry["domain"]].append(lemma)

    def candidates(verb, role):
        """Attested partners first, then everything sharing a compatible domain.

        Direct collocation is better evidence but thin - only 108 of 222 verbs have a
        content-word object anywhere in the corpus - so domain compatibility carries the rest."""
        attested = [w for w in lemma_pairs[role][verb] if w in vocabulary]
        verb_domain = domains.get(verb)
        compatible = []
        if verb_domain:
            for argument_domain in domain_pairs[role].get(verb_domain, ()):
                compatible.extend(nouns_by_domain.get(argument_domain, ()))
        ordered = attested + [w for w in compatible if w not in attested]
        return ordered

    verbs = {}
    for lemma, nodes in corpus.items():
        if part_of_speech[lemma] != "verb" or len(nodes) < MIN_VERB:
            continue
        voices = {api.F.voice.v(n) for n in nodes} - {None}
        verbs[lemma] = {
            "key": lemma,
            "gloss": glosses[lemma],
            "frequency": len(nodes),
            "domain": domains[lemma],
            "government": _government(object_cases[lemma]),
            "moods": sorted({api.F.mood.v(n) for n in nodes} - {None}),
            "tenses": sorted({api.F.tense.v(n) for n in nodes} - {None}),
            "voices": sorted(voices),
            "deponent": bool(voices) and "active" not in voices,
            "prepositions": [p for p, _ in prepositions[lemma].most_common(6)],
            "subject_lexemes": candidates(lemma, "s"),
            "object_lexemes": candidates(lemma, "o"),
        }

    substantives = {lemma: {
        "key": lemma,
        "gloss": entry["gloss"],
        "frequency": entry["frequency"],
        "domain": entry["domain"],
        "gender": entry.get("gender"),
        "proper": entry.get("proper", False),
        "natural_frame": entry.get("natural_frame", []),
    } for lemma, entry in vocabulary.items() if entry["part_of_speech"] == "noun"}

    return vocabulary, {"verbs": verbs, "substantives": substantives}


def write():
    vocabulary, elements = build()

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
    ELEMENTS_PATH.write_text(json.dumps(elements, ensure_ascii=False, indent=1), encoding="utf-8")
    return len(vocabulary), len(elements["verbs"]), len(elements["substantives"])


if __name__ == "__main__":
    print("vocabulary %d | verbs %d | substantives %d" % write())

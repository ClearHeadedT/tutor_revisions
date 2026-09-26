"""Builds corpus_index.json, the N1904 data a card is checked against and prefetched from.

    python -m text_fabric.corpus_index

One corpus pass, so nothing downstream has to open Text-Fabric. It keeps:

  verses       every verse's words, folded (no accents or case, see greek_text.fold_greek), and
               their lemmas, in order - what the echo check compares a sentence with
  form_lemma   each folded form's commonest lemma, to lemmatize a sentence given without lemmas
  lemmas       each lemma's frequency, class and gloss - what counts as a content word, and what a
               student is shown for a word they have not met
  morphology   every verb counted by tense, voice and mood, so a sentence plan picks between the
               charts a construction could be built from in proportion to how the corpus builds it
  analyses     every form as written (accented, grave read as acute, lower case) with each lemma
               and parse it carries in the corpus, and how often - what a card's words are checked
               against, one form at a time
  frames       for each verb, the cases of its objects and the prepositions heading its adverbial
               phrases, counted over clauses where it is the only verb, so neither can belong to
               another verb
"""

import collections
import json
import unicodedata
from functools import cache
from pathlib import Path

from greek_text import fold_greek, normalize_greek
from text_fabric.fabric_utils import load_n1904

INDEX_PATH = Path("data/curriculum_data/corpus_index.json")

PERSONS = {"p1": "1st person", "p2": "2nd person", "p3": "3rd person"}
# How an uninflected word is described, by part of speech.
UNINFLECTED = {"conj": "conjunction", "prep": "preposition", "advb": "adverb", "intj": "interjection",
               "art": "article", "adjv": "adjective", "subs": "noun", "pron": "pronoun", "num": "numeral",
               "verb": "verb"}


def written_form(text):
    """A form as the analyses are keyed: NFC, lower case, a grave accent read as the acute it
    stands for. Two spellings differing only in a grave are the same word."""
    decomposed = unicodedata.normalize("NFD", normalize_greek(text).strip().lower())
    return unicodedata.normalize("NFC", decomposed.replace("̀", "́"))


def parse_of(F, word):
    """A word's parse in the grammars' own order and wording, e.g. "aorist active indicative 3rd
    person singular" or "present active participle genitive feminine singular"."""
    voice = F.voice.v(word)
    parts = [F.tense.v(word), "middle/passive" if voice == "middlepassive" else voice, F.mood.v(word),
             PERSONS.get(F.person.v(word)), F.case.v(word), F.gender.v(word), F.number.v(word)]
    return " ".join(part for part in parts if part) or UNINFLECTED.get(F.sp.v(word), F.sp.v(word) or "")


def _frames(api):
    """Each verb's object cases and adverbial prepositions. role sits on the constituent - the
    phrase or word group - not on its words, so each constituent the clause holds directly is read
    whole: its case from its first inflected word, its preposition from its first word."""
    F, L, E = api.F, api.L, api.E
    objects = collections.defaultdict(collections.Counter)
    prepositions = collections.defaultdict(collections.Counter)
    for clause in F.otype.s("clause"):
        children = E.parent.t(clause)
        verbs = [c for c in children if F.otype.v(c) == "word" and F.sp.v(c) == "verb"]
        if len(verbs) != 1:
            continue
        verb = normalize_greek(F.lemma.v(verbs[0]) or "")
        for child in children:
            words = [child] if F.otype.v(child) == "word" else list(L.d(child, otype="word"))
            role = F.role.v(child)
            if role in ("o", "o2"):
                case = next((F.case.v(w) for w in words if F.case.v(w)), None)
                if case in ("genitive", "dative", "accusative"):
                    objects[verb][case] += 1
            elif role == "adv" and words and F.sp.v(words[0]) == "prep":
                case = next((F.case.v(w) for w in words[1:] if F.case.v(w)), None)
                if case:
                    prepositions[verb][f"{normalize_greek(F.lemma.v(words[0]))} + {case}"] += 1
    return {verb: {"objects": dict(objects[verb].most_common()),
                   "prepositions": dict(prepositions[verb].most_common(8))}
            for verb in set(objects) | set(prepositions)}


def build():
    api = load_n1904().api
    F, L, T = api.F, api.L, api.T

    verses = []
    morphology = collections.Counter()
    form_lemmas = collections.defaultdict(collections.Counter)
    analyses = collections.defaultdict(collections.Counter)
    lemma_nodes = collections.defaultdict(list)
    for verse in F.otype.s("verse"):
        book, chapter, number = T.sectionFromNode(verse)
        tokens, lemmas = [], []
        for word in L.d(verse, otype="word"):
            form = fold_greek(F.text.v(word) or "")
            lemma = normalize_greek(F.lemma.v(word) or "")
            if not form or not lemma:
                continue
            tokens.append(form)
            lemmas.append(lemma)
            form_lemmas[form][lemma] += 1
            analyses[written_form(F.text.v(word))][(lemma, parse_of(F, word))] += 1
            lemma_nodes[lemma].append(word)
            if F.sp.v(word) == "verb":
                morphology[f"{F.tense.v(word)}|{F.voice.v(word)}|{F.mood.v(word)}"] += 1
        verses.append([f"{book} {chapter}:{number}", tokens, lemmas])

    lemma_info = {}
    for lemma, nodes in lemma_nodes.items():
        glosses = [F.gloss.v(n) for n in nodes if F.gloss.v(n)]
        lemma_info[lemma] = {
            "frequency": len(nodes),
            "cls": collections.Counter(F.cls.v(n) for n in nodes).most_common(1)[0][0],
            "gloss": max(glosses, key=len) if glosses else None,
        }

    return {
        "source": {"corpus": "CenterBLC/N1904", "folding": "greek_text.fold_greek"},
        "verses": verses,
        "form_lemma": {form: counts.most_common(1)[0][0] for form, counts in form_lemmas.items()},
        "lemmas": lemma_info,
        "morphology": dict(morphology.most_common()),
        "analyses": {form: [[lemma, parse, n] for (lemma, parse), n in counts.most_common()]
                     for form, counts in analyses.items()},
        "frames": _frames(api),
    }


@cache
def load_corpus_index():
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def write():
    index = build()
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return len(index["verses"]), len(index["analyses"]), len(index["frames"])


if __name__ == "__main__":
    print("verses %d | written forms %d | verb frames %d" % write())

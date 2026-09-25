"""Builds corpus_index.json, the N1904 text a finished card is checked against for echo.

    python -m text_fabric.corpus_index

One corpus pass, so the check itself never has to open Text-Fabric. For every verse it keeps the
words folded (no accents or case, see greek_text.fold_greek) and their lemmas, in order. Alongside
those it keeps two lookups: each folded form's commonest lemma, which lemmatizes a sentence whose
lemmas were not supplied, and each lemma's frequency, class and gloss, which decide what counts as a
content word and what a student is shown for a word they have not met.

It also counts every verb by tense, voice and mood, which is how a sentence plan picks between the
charts a construction could be built from: in proportion to how often the corpus builds it that way.
"""

import collections
import json
from functools import cache
from pathlib import Path

from greek_text import fold_greek, normalize_greek
from text_fabric.fabric_utils import load_n1904

INDEX_PATH = Path("data/curriculum_data/corpus_index.json")


def build():
    api = load_n1904().api
    F, L, T = api.F, api.L, api.T

    verses = []
    morphology = collections.Counter()
    form_lemmas = collections.defaultdict(collections.Counter)
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
    }


@cache
def load_corpus_index():
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def write():
    index = build()
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return len(index["verses"]), len(index["form_lemma"]), len(index["lemmas"])


if __name__ == "__main__":
    print("verses %d | forms %d | lemmas %d" % write())

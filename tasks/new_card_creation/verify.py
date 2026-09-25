"""Deterministic checks on a generated card, run before it is kept. No model call.

Two questions are asked of the sentence:

  echo        Does it reproduce the Greek New Testament? Measured twice, because a card can fail
              two ways. `longest_shared_run` catches lifted wording: the longest run of words the
              sentence shares with the corpus, spelling folded so an accent or a capital does not
              hide it. `closest_passage` catches a retold scene, which shares content words with one
              passage but not their order - βαπτίζω, ποταμός, ὁμολογέω, ἁμαρτία is Mark 1:5 however
              the clauses are arranged.

  vocabulary  Does it reach past what the student knows? Soft: a word or two outside the list is
              kept and glossed on the card; more than that sends the card back.

The thresholds were set against the 25 audited cards in testing/output*, where the auditor's
verdicts serve as labels. At these values the passage check caught 7 of the 9 echo failures and
none of the clean cards, but the margin to the clean cards was thin (13.9 against 14) and the sample
small, so treat them as a first setting to revisit as generated cards accumulate.
"""

import math
from functools import cache

from greek_text import fold_greek, greek_tokens, normalize_greek
from text_fabric.corpus_index import load_corpus_index

# Word classes that carry no scene of their own. They are ignored when passages are compared on
# content, and never count as vocabulary a student has to have met.
CLOSED_CLASSES = {"det", "conj", "prep", "pron", "ptcl"}
NEGATIVES = {"οὐ", "μή"}
# Lemmas this common appear in every scene, so sharing them with a passage says nothing about it.
CONTENT_CEILING = 500
# How many consecutive verses a retold scene may be spread across.
PASSAGE_WINDOW = 3

# A shared run this long is flagged when it holds at least one content word; runs of function
# words alone (ἐν τῇ, καὶ ὁ) are ordinary Greek and say nothing.
RUN_LIMIT = 4
# Shared content lemmas are weighed by rarity, ln(verses / verses containing the lemma), since
# sharing ποταμός with a passage says far more than sharing ἀκούω. The sum is compared with this.
PASSAGE_LIMIT = 14.0
UNKNOWN_LIMIT = 2


@cache
def corpus():
    """The index plus the two lookups built from it: every position of every folded word in one
    running stream, and the verses each lemma occurs in."""
    index = load_corpus_index()
    stream, verse_of, positions = [], [], {}
    lemma_verses = {}
    for number, (_, tokens, lemmas) in enumerate(index["verses"]):
        for token in tokens:
            positions.setdefault(token, []).append(len(stream))
            stream.append(token)
            verse_of.append(number)
        for lemma in set(lemmas):
            lemma_verses.setdefault(lemma, []).append(number)
    folded_lemmas = {fold_greek(lemma): lemma for lemma in index["lemmas"]}
    total = len(index["verses"])
    rarity = {lemma: math.log(total / len(verses)) for lemma, verses in lemma_verses.items()}
    return {**index, "stream": stream, "verse_of": verse_of, "positions": positions,
            "lemma_verses": lemma_verses, "folded_lemmas": folded_lemmas, "rarity": rarity}


def canonical_lemma(lemma):
    """A lemma as the corpus spells it, or the input unchanged when the corpus lacks it."""
    return corpus()["folded_lemmas"].get(fold_greek(lemma), normalize_greek(lemma))


def lemmatize(sentence):
    """The lemma of each word the corpus attests, by the commonest reading of its folded form.
    Used when the model did not supply lemmas; a form the corpus never has is passed over."""
    form_lemma = corpus()["form_lemma"]
    return [form_lemma[token] for token in greek_tokens(sentence) if token in form_lemma]


def is_closed_class(lemma):
    info = corpus()["lemmas"].get(lemma)
    return lemma in NEGATIVES or (info is not None and info["cls"] in CLOSED_CLASSES)


def is_content(lemma):
    info = corpus()["lemmas"].get(lemma)
    if info is None:
        return True
    return info["cls"] not in CLOSED_CLASSES and lemma not in NEGATIVES \
        and info["frequency"] <= CONTENT_CEILING


def longest_shared_run(sentence):
    """The longest run of consecutive words the sentence shares with the corpus, and where, with
    whether it holds a content word."""
    c = corpus()
    tokens = greek_tokens(sentence)
    best = {"length": 0, "ref": None, "words": []}
    for start, token in enumerate(tokens):
        for position in c["positions"].get(token, ()):
            length = 1
            while (start + length < len(tokens) and position + length < len(c["stream"])
                   and c["stream"][position + length] == tokens[start + length]):
                length += 1
            if length > best["length"]:
                best = {"length": length, "ref": c["verses"][c["verse_of"][position]][0],
                        "words": tokens[start:start + length]}
    form_lemma = c["form_lemma"]
    best["has_content"] = any(is_content(form_lemma[word]) for word in best["words"] if word in form_lemma)
    return best


def closest_passage(lemmas, target=None):
    """The run of up to PASSAGE_WINDOW verses whose shared content lemmas weigh most.

    target is the lemma the card is about. It is left out, since the card has to use it and it
    would otherwise point every card at the passages its word is famous for."""
    c = corpus()
    content = {canonical_lemma(lemma) for lemma in lemmas} - {canonical_lemma(target or "")}
    content = {lemma for lemma in content if is_content(lemma)}
    hits = {}
    for lemma in content:
        for verse in c["lemma_verses"].get(lemma, ()):
            for start in range(verse - PASSAGE_WINDOW + 1, verse + 1):
                hits.setdefault(start, set()).add(lemma)
    best = {"score": 0.0, "ref": None, "lemmas": []}
    for start, shared in hits.items():
        score = round(sum(c["rarity"][lemma] for lemma in shared), 1)
        if start < 0 or score <= best["score"]:
            continue
        refs = [c["verses"][n][0] for n in range(start, min(start + PASSAGE_WINDOW, len(c["verses"])))]
        # a window may not run across a chapter boundary
        if len({ref.rsplit(":", 1)[0] for ref in refs}) > 1:
            continue
        best = {"score": score, "ref": f"{refs[0]}-{refs[-1].rsplit(':', 1)[1]}",
                "lemmas": sorted(shared)}
    return best


def unknown_lemmas(lemmas, student):
    """Open-class lemmas the student has not met, each with the gloss a card can show for it."""
    known = {fold_greek(lemma) for lemma in student.vocabulary}
    unknown = {}
    for lemma in lemmas:
        lemma = canonical_lemma(lemma)
        if fold_greek(lemma) in known or is_closed_class(lemma):
            continue
        unknown[lemma] = (corpus()["lemmas"].get(lemma) or {}).get("gloss")
    return unknown


def check_card(card, student=None, target=None):
    """Every finding against one card, and the measurements they rest on.

    findings is empty when the card can be kept. helps carries the glosses for the few unknown
    words a card is allowed; it is None when the student's vocabulary was not checked. target is
    the card's own lemma, for a vocabulary card."""
    sentence = card.get("sentence", "")
    lemmas = card.get("lemmas") or lemmatize(sentence)
    run = longest_shared_run(sentence)
    passage = closest_passage(lemmas, target)
    findings = []
    if run["length"] >= RUN_LIMIT and run["has_content"]:
        findings.append(f"The sentence shares {run['length']} consecutive words with {run['ref']} "
                        f"({' '.join(run['words'])}). Write it in your own words.")
    if passage["score"] >= PASSAGE_LIMIT:
        findings.append(f"The sentence shares the content words {', '.join(passage['lemmas'])} with "
                        f"{passage['ref']}, which reads as a retelling of that passage. Build a "
                        f"different scene inside the setting you were given.")
    helps = None
    if student is not None:
        helps = unknown_lemmas(lemmas, student)
        if len(helps) > UNKNOWN_LIMIT:
            findings.append(f"The sentence uses {len(helps)} words outside the student's vocabulary "
                            f"({', '.join(helps)}); at most {UNKNOWN_LIMIT} are allowed.")
    return {"findings": findings, "helps": helps,
            "overlap": {"longest_run": run, "closest_passage": passage}}

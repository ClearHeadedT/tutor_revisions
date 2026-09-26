"""Checks on a generated card, from the corpus alone. No model call.

  form        Each word, on its own, against every analysis N1904 gives that written form: lemma,
              parse and accent. A verb form or target the GNT never uses is sent back with the
              forms it does use; any other unattested word is only noted. A grammar card's target
              must be one of the item's GNT forms and carry its parse, a vocabulary card's must be
              a form of its word.

  lexemes     A syntax card's construction must be built on one of the item's GNT pairings.

  withheld    God, Christ, angels and demons, and religious and ethnic groups and offices never appear,
              except as a vocabulary card's own word, and then not in the nominative or vocative.

  vocabulary  A word or two outside the student's list is kept and glossed; more sends it back.
"""

import re
from functools import cache

from greek_text import fold_greek, greek_tokens, greek_words, normalize_greek
from text_fabric.corpus_index import load_corpus_index, written_form

# Word classes that carry no scene of their own. They are ignored when passages are compared on
# content, and never count as vocabulary a student has to have met.
CLOSED_CLASSES = {"det", "conj", "prep", "pron", "ptcl"}
NEGATIVES = {"οὐ", "μή"}
UNKNOWN_LIMIT = 2

# Persons, beings and groups a card could render offensively or inappropriately: the divine and the
# demonic, and the religious and ethnic groups and offices of the New Testament's narrative. Nothing
# supplied to the model uses them, and a card using them is sent back.
WITHHELD = {fold_greek(lemma) for lemma in (
    "θεός", "θεά", "Ἰησοῦς", "Χριστός", "Μεσσίας", "ἀντίχριστος", "ψευδόχριστος",
    "ἄγγελος", "ἀρχάγγελος", "Σατανᾶς", "διάβολος", "δαιμόνιον", "δαίμων", "Βεελζεβούλ", "Βελιάρ",
    "Ἰουδαῖος", "Φαρισαῖος", "Σαδδουκαῖος", "Σαμαρίτης", "Σαμαρῖτις", "Ἰσραήλ", "Ἰσραηλίτης",
    "Ἑβραῖος", "Ναζωραῖος", "Ναζαρηνός", "Χριστιανός", "Ἡρῳδιανοί", "Ἕλλην", "ἔθνος", "ἐθνικός",
    "προσήλυτος", "περιτομή", "ἀκροβυστία",
    "ἀρχιερεύς", "γραμματεύς", "ἀπόστολος", "προφήτης", "ψευδοπροφήτης", "Λευίτης", "ἀρχισυνάγωγος",
    "ἐκκλησία", "σταυρός")}


@cache
def corpus():
    """The index, with its lemmas also looked up by folded spelling."""
    index = load_corpus_index()
    return {**index, "folded_lemmas": {fold_greek(lemma): lemma for lemma in index["lemmas"]}}


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


# ---- form ------------------------------------------------------------------------------------

# N1904 files the future of λέγω under εἶπον; a model will call it λέγω.
LEMMA_ALIASES = {fold_greek("εἶπον"): fold_greek("λέγω")}

# The words a parse is read from, whatever order or wording it comes in. Middle and passive are
# read only as "not active": the corpus tags many forms middle/passive and deponents either way, so
# a finer distinction would send back cards that are right.
PARSE_WORDS = {
    **{tense: ("tense", tense) for tense in ("present", "imperfect", "future", "aorist", "perfect", "pluperfect")},
    "active": ("voice", "active"), "middle": ("voice", "not active"), "passive": ("voice", "not active"),
    **{mood: ("mood", mood) for mood in ("indicative", "subjunctive", "optative", "imperative",
                                          "infinitive", "participle")},
    **{case: ("case", case) for case in ("nominative", "genitive", "dative", "accusative", "vocative")},
    **{gender: ("gender", gender) for gender in ("masculine", "feminine", "neuter")},
    "singular": ("number", "singular"), "plural": ("number", "plural"),
    "1st": ("person", "1"), "first": ("person", "1"), "2nd": ("person", "2"), "second": ("person", "2"),
    "3rd": ("person", "3"), "third": ("person", "3"),
}
# "first aorist", "second declension" and the like name no person.
NOT_PERSONS = {"aorist", "future", "perfect", "passive", "declension"}


def parse_features(text):
    """The features a parse names: tense, voice, mood, person, case, gender, number."""
    tokens = [token for token in re.split(r"[\s_/,;:.()\-]+", (text or "").lower()) if token]
    features = {}
    for index, token in enumerate(tokens):
        if token in ("1st", "first", "2nd", "second") and tokens[index + 1:index + 2] and \
                tokens[index + 1] in NOT_PERSONS:
            continue
        if token in PARSE_WORDS:
            name, value = PARSE_WORDS[token]
            features.setdefault(name, value)
    return features


def compatible(claimed, attested):
    """True when no feature both parses name is named differently."""
    return all(attested[name] == value for name, value in claimed.items() if name in attested)


def same_lemma(one, other):
    one, other = fold_greek(one or ""), fold_greek(other or "")
    return LEMMA_ALIASES.get(one, one) == LEMMA_ALIASES.get(other, other)


@cache
def accent_variants():
    """Every written form, grouped by its folded spelling: the forms a word could be if only its
    accents or breathings are off."""
    grouped = {}
    for form in load_corpus_index()["analyses"]:
        grouped.setdefault(fold_greek(form), []).append(form)
    return grouped


def analyses_of(word):
    """The corpus's analyses of a word as [lemma, parse, count], and whether they were found only
    by ignoring its accents. None when the corpus never has the word at all."""
    index = load_corpus_index()["analyses"]
    if written_form(word) in index:
        return index[written_form(word)], False
    variants = accent_variants().get(fold_greek(word))
    if variants:
        return [analysis for variant in variants for analysis in index[variant]], True
    return None, False


@cache
def verb_forms():
    """{folded lemma: [(form, tense, voice, mood, parse, count)]} for every verb form in the corpus."""
    grouped = {}
    for form, analyses in load_corpus_index()["analyses"].items():
        for lemma, parse, count in analyses:
            words = parse.split()
            if len(words) >= 3 and words[2] in ("indicative", "subjunctive", "optative", "imperative",
                                                "infinitive", "participle"):
                folded = fold_greek(lemma)
                grouped.setdefault(LEMMA_ALIASES.get(folded, folded), []).append(
                    (form, words[0], words[1], words[2], parse, count))
    return grouped


def attested_alternatives(lemma, parse, count=5):
    """The GNT's forms of a verb in the tense and mood a parse names, commonest first."""
    wanted = parse_features(parse)
    forms = verb_forms().get(LEMMA_ALIASES.get(fold_greek(lemma or ""), fold_greek(lemma or "")), [])
    same = [f for f in forms if f[1] == wanted.get("tense") and f[3] == wanted.get("mood")]
    return [f"{form} ({parse})" for form, _, _, _, parse, _ in sorted(same, key=lambda f: -f[5])[:count]]


def not_in_gnt(word, claim):
    alternatives = attested_alternatives(claim.get("lemma"), claim.get("parse"))
    return (f"{word} is not a form the GNT has. Use one it does"
            + (f"; its {parse_features(claim.get('parse')).get('tense', '')} "
               f"{parse_features(claim.get('parse')).get('mood', '')} forms of {claim.get('lemma')} are: "
               f"{'; '.join(alternatives)}." if alternatives else "."))


def describe(analyses):
    return "; ".join(f"{parse} of {lemma}" for lemma, parse, _ in analyses[:4])


def check_words(card):
    """Each word of the sentence against the corpus. Returns the findings that send the card back,
    notes for the record, and a verdict for every word."""
    claims = {}
    for entry in card.get("words") or []:
        if isinstance(entry, dict) and entry.get("form"):
            claims.setdefault(written_form(entry["form"]), entry)
    findings, notes, verdicts = [], [], []
    missing = [word for word in greek_words(card.get("sentence", "")) if written_form(word) not in claims]
    if missing:
        findings.append(f"These words of the sentence are missing from \"words\": {', '.join(missing)}. "
                        f"Give every word with its lemma and parse, so each can be checked.")
    for word in greek_words(card.get("sentence", "")):
        claim = claims.get(written_form(word))
        verdict = {"form": word}
        if claim:
            verdict["given"] = f"{claim.get('parse')} of {claim.get('lemma')}"
        analyses, by_spelling = analyses_of(word)
        if analyses is None:
            if claim and "mood" in parse_features(claim.get("parse")):
                findings.append(not_in_gnt(word, claim))
                verdicts.append({**verdict, "status": "verb form not in the GNT"})
            else:
                verdicts.append({**verdict, "status": "unverified: not in the GNT"})
            continue
        if by_spelling:
            # The GNT carries the enclitic accents too (ἄνθρωπός τις), so a form it never writes this
            # way is almost always mis-accented.
            findings.append(f"{word} is not accented as the GNT writes it: it has "
                            f"{', '.join(accent_variants()[fold_greek(word)][:3])}.")
        if claim is None:
            verdicts.append({**verdict, "status": "attested, no parse given"})
            continue
        wanted = parse_features(claim.get("parse"))
        if any(same_lemma(lemma, claim.get("lemma")) and compatible(wanted, parse_features(parse))
               for lemma, parse, _ in analyses):
            verdicts.append({**verdict, "status": "confirmed" + (" (accent differs)" if by_spelling else "")})
            continue
        verdicts.append({**verdict, "status": "mismatch", "gnt": describe(analyses)})
        findings.append(f"{word} is given as {claim.get('parse')} of {claim.get('lemma')}, but the GNT "
                        f"has this form only as {describe(analyses)}. Either the form or its parse is "
                        f"wrong; correct whichever it is.")
    return findings, notes, verdicts


def check_target(card, target=None, target_features=None, target_forms=None):
    """The card's target, held to its item: a form the GNT has, of the vocabulary word or carrying
    the grammar item's parse, and for a grammar item one of the GNT forms it offers. An unattested
    verb target is already sent back by check_words."""
    form = (card.get("target_form") or "").strip()
    words = greek_words(form)
    if not words:
        return ["target_form is empty."], []
    if written_form(words[0]) not in {written_form(w) for w in greek_words(card.get("sentence", ""))}:
        return [f"target_form {form} does not appear in the sentence."], []
    if target_forms and fold_greek(words[0]) not in {fold_greek(option) for option in target_forms}:
        return [f"The target {form} is not one of the item's New Testament forms "
                f"({', '.join(target_forms)}). Build the card on one of them."], []
    if len(words) > 1 or not (target or target_features):
        return [], []
    word = words[0]
    claim = next((entry for entry in card.get("words") or [] if isinstance(entry, dict)
                  and written_form(entry.get("form", "")) == written_form(word)), {})
    analyses, _ = analyses_of(word)
    if analyses is None:
        return [] if "mood" in parse_features(claim.get("parse")) else [not_in_gnt(word, claim)], []
    note = []
    if target and not any(same_lemma(lemma, target) for lemma, _, _ in analyses):
        return [f"The target {word} is not a form of {target}: the GNT has it as {describe(analyses)}."], note
    if target_features:
        wanted = parse_features(" ".join(str(value) for value in target_features.values()))
        if not any(compatible(wanted, parse_features(parse)) for _, parse, _ in analyses):
            return [f"The target {word} does not carry the item's parse "
                    f"({' '.join(str(v) for v in target_features.values())}); the GNT has it as "
                    f"{describe(analyses)}."], note
    return [], note


def check_lexemes(card, lemmas, options):
    """A syntax card, held to its item: the construction is built on one of the pairings the GNT
    uses for it. A word counts by the lemma given for it or any lemma the corpus gives its form."""
    found = set(lemmas)
    for word in greek_words(card.get("sentence", "")):
        found |= {lemma for lemma, _, _ in analyses_of(word)[0] or []}
    if any(all(any(same_lemma(value, lemma) for lemma in found) for value in option.values()) for option in options):
        return []
    return [f"The sentence is not built on any of the item's New Testament pairings "
            f"({'; '.join(' + '.join(option.values()) for option in options)}). Build the construction on one of them."]


def check_withheld(card, target=None):
    """Withheld words, by the lemma given for each word or any lemma the corpus gives its form. A
    vocabulary card's own word may stand, but not in the nominative or vocative, where it would act
    or speak."""
    claims = {written_form(entry.get("form", "")): entry for entry in card.get("words") or []
              if isinstance(entry, dict)}
    findings = []
    for word in greek_words(card.get("sentence", "")):
        claim = claims.get(written_form(word), {})
        lemmas = {claim.get("lemma") or ""} | {lemma for lemma, _, _ in analyses_of(word)[0] or []}
        withheld = next((lemma for lemma in lemmas if fold_greek(lemma) in WITHHELD), None)
        if not withheld:
            continue
        if target and same_lemma(withheld, target):
            if parse_features(claim.get("parse")).get("case") in ("nominative", "vocative"):
                findings.append(f"{word}: the item may appear here only outside the nominative and "
                                f"vocative, never as the one who acts or speaks. Recast the sentence.")
        else:
            findings.append(f"{word} ({withheld}) is withheld from these cards: a sentence may not name "
                            f"God, Christ, angels or demons, or a religious or ethnic group or office. "
                            f"Rewrite it without it.")
    return findings


# ---- the card --------------------------------------------------------------------------------

def check_card(card, student=None, target=None, target_features=None, target_forms=None, target_lexemes=None):
    """Every finding against one card, and the measurements they rest on.

    findings is empty when the card can be kept. helps carries the glosses for the few unknown
    words a card is allowed; it is None when the student's vocabulary was not checked. target is
    the card's own lemma, for a vocabulary card; target_features the item's features and
    target_forms its GNT forms, for a grammar card; target_lexemes its GNT pairings, for a syntax
    card."""
    sentence = card.get("sentence", "")
    given = [entry.get("lemma") for entry in card.get("words") or [] if isinstance(entry, dict)]
    lemmas = [lemma for lemma in given if lemma] or card.get("lemmas") or lemmatize(sentence)
    findings = []
    form_findings, notes, verdicts = check_words(card)
    target_findings, target_notes = check_target(card, target, target_features, target_forms)
    findings += target_findings + form_findings + check_withheld(card, target)
    if target_lexemes:
        findings += check_lexemes(card, lemmas, target_lexemes)
    helps = None
    if student is not None:
        # the item under review is being learned; it never counts against the student's vocabulary
        helps = unknown_lemmas([lemma for lemma in lemmas if not same_lemma(lemma, target)], student)
        if len(helps) > UNKNOWN_LIMIT:
            findings.append(f"The sentence uses {len(helps)} words outside the student's vocabulary "
                            f"({', '.join(helps)}); at most {UNKNOWN_LIMIT} are allowed.")
    return {"findings": findings, "notes": target_notes + notes, "helps": helps, "words": verdicts}

"""Builds grammar_scaffolding.json from the paradigm charts the builder recovered.

**Why not Text-Fabric.** TF carries every attested form with full parsing, which makes it the
right source for lexical data and the wrong one for paradigms: only 18 verbs attest all six
present active indicative forms, exactly one attests all six imperfect active indicative, and
λύω - the paradigm verb every grammar uses precisely because it is regular - barely occurs in
the corpus at all. A teaching paradigm is not something the New Testament contains. It is
something a grammar prints, which is where these come from. TF is used afterwards, for what a
chart cannot say: which of its slots the GNT actually uses, and the GNT's own forms of each.

**Where the identity comes from.** The builder's typed paradigms carry forms but not tense,
voice or mood, and the lead form cannot supply it either - λύσω is attested once in the corpus
and it is an aorist subjunctive, not the future indicative Mounce intends by it. The identity
comes from the chart's own headings. BBGG's appendix prints four Overview charts in a
consistent column-major shape:

    Overview of Indicative
      present / imperfect / future / 1st aorist / 2nd aorist / perfect   <- tense columns
      active indicative                                                 <- voice section
      1 sg                                                              <- row label
      λύω / ἔλυον / λύσω / ἔλυσα / ἔλαβον / λέλυκα                       <- one form per column

Read that way, tense, voice, mood and person/number are all stated rather than inferred.

**Beyond λύω.** The Overviews give the paradigm verb only. The rest of the appendix prints the same
tenses on the verbs λύω stands in for - contract, liquid and athematic - with every participle, and
the declension, adjective and pronoun charts. Those grids read cleanly from the body text, but
which verb, tense and voice a column holds does not, so APPENDIX_VERBS and APPENDIX_NOMINALS
declare it grid by grid, in the order the appendix prints them. A handful of cells the export or
the printing damaged are corrected in CORRECTIONS, each named, rather than passed on to the model
as authoritative.

**Rule, pattern, slot.** A rule (pres-act-ind, decl3) holds a pattern for each chart heading the
appendix prints under it (thematic, contract-έω, n-3c(4)), and a pattern holds its slots. The item a
student reviews is a slot of a pattern: one morphological fact, never a mix of two.
"""

import collections
import json
import os
import re
import unicodedata
from pathlib import Path

from greek_text import fold_greek, normalize_greek
from tasks.new_card_creation.verify import WITHHELD

BUILDER = Path("/home/austin/repos/koine-grammar-builder")
GRAMMAR_PATH = Path("data/curriculum_data/grammar_scaffolding.json")

PERSON_NUMBER = {
    "1 sg": ("first_person", "singular"), "2 sg": ("second_person", "singular"),
    "3 sg": ("third_person", "singular"), "1 pl": ("first_person", "plural"),
    "2 pl": ("second_person", "plural"), "3 pl": ("third_person", "plural"),
}
CASE_NUMBER = [("nominative", "singular"), ("genitive", "singular"), ("dative", "singular"),
               ("accusative", "singular"), ("nominative", "plural"), ("genitive", "plural"),
               ("dative", "plural"), ("accusative", "plural")]

# Chart wording -> (feature value, key fragment). "1st aorist" and "2nd aorist" are the same
# tense formed two ways, so they share a feature value and differ only in the key.
TENSES = {
    "present": ("present", "pres"), "imperfect": ("imperfect", "impf"),
    "future": ("future", "fut"), "perfect": ("perfect", "perf"),
    "1st aorist": ("aorist", "aor1"), "first aorist": ("aorist", "aor1"),
    "2nd aorist": ("aorist", "aor2"), "second aorist": ("aorist", "aor2"),
    "future inf": ("future", "fut"),
}
VOICES = {"active": "act", "middle": "mid", "passive": "pas", "middle/passive": "midpas"}
MOODS = {"indicative": "ind", "subjunctive": "subj", "imperative": "impv", "infinitive": "inf",
         "participle": "ptc"}
ASPECTS = {"present": "continuous", "imperfect": "continuous", "future": "undefined",
           "aorist": "undefined", "perfect": "completed"}
ORDINAL = {"first_person": "1st person", "second_person": "2nd person",
           "third_person": "3rd person"}

# Where each chart sits in BBGG's appendix, and what shape it has.
OVERVIEWS = [
    ("Overview of Indicative", "indicative", PERSON_NUMBER),
    ("Overview of Subjunctive", "subjunctive", PERSON_NUMBER),
    ("Overview of Imperative", "imperative",
     {k: v for k, v in PERSON_NUMBER.items() if k.startswith(("2", "3"))}),
    ("Overview of Infinitive", "infinitive", None),   # no person or number
]


def _body_lines():
    import sys
    sys.path.insert(0, str(BUILDER))
    from structure.profile import ResourceProfile
    from structure.text_source import TextSource
    source = TextSource(ResourceProfile.load("BBGG"))
    return [(line.text if hasattr(line, "text") else str(line)).strip()
            for line in source.body_lines]


def _read_overview(lines, start, mood, row_labels):
    """One Overview chart, as {(tense_key, voice): {slot: form}}.

    The chart names its tense columns once, then repeats a voice section for each voice, and
    inside a section names a row and lists one form per tense column."""
    tenses, sections, voice = [], {}, None
    pending_slot, index = None, start + 1

    while index < len(lines):
        line = lines[index]
        index += 1
        if not line:
            continue
        lowered = line.lower()
        if lowered.startswith("overview of"):
            break
        if lowered in TENSES and not voice:
            # A tense header after a voice section has already been filled belongs to the next
            # chart, not this one. The infinitive chart is followed immediately by eimi's, whose
            # columns would otherwise be read as four more tenses of the infinitive.
            if sections:
                break
            tenses.append(TENSES[lowered])
            continue
        spoken = lowered.replace(f" {mood}", "").strip()
        if spoken in VOICES and (mood == "infinitive" or f" {mood}" in lowered):
            voice = VOICES[spoken]
            pending_slot = [] if row_labels is None else None
            sections.setdefault(voice, {})
            continue
        if voice is None:
            continue
        if row_labels is not None and lowered in row_labels:
            pending_slot = row_labels[lowered]
            sections[voice][pending_slot] = []
            continue
        if row_labels is None:
            sections[voice].setdefault("_", []).append(line)
            if len(sections[voice]["_"]) >= len(tenses):
                voice = None
        elif pending_slot is not None:
            sections[voice][pending_slot].append(line)

    charts = {}
    for voice, rows in sections.items():
        for column, (tense, tense_key) in enumerate(tenses):
            slots = {}
            for slot, forms in rows.items():
                if column < len(forms):
                    slots[slot] = forms[column]
            if slots:
                charts[(tense_key, tense, voice)] = slots
    return charts, index


def _eimi(lines, start):
    """εἰμί's indicative, printed with its own three tense columns after the infinitive chart."""
    tenses, rows, slot = [], {}, None
    for index in range(start, start + 60):
        line = lines[index]
        if not line:
            continue
        lowered = line.lower()
        if lowered == "indicative":
            continue
        if lowered in TENSES and not rows:
            tenses.append(TENSES[lowered]); continue
        if lowered in PERSON_NUMBER:
            slot = PERSON_NUMBER[lowered]; rows[slot] = []; continue
        if slot and len(rows[slot]) < len(tenses):
            rows[slot].append(line)
        elif rows and all(len(v) >= len(tenses) for v in rows.values()) and len(rows) >= 6:
            break
    charts = {}
    for column, (tense, tense_key) in enumerate(tenses):
        slots = {s: f[column] for s, f in rows.items() if column < len(f)}
        if slots:
            charts[(tense_key, tense, "act")] = slots
    return charts


# ---- the appendix grids ---------------------------------------------------------------------------

ROW_SLOTS = {**PERSON_NUMBER,
             "nom sg": ("nominative", "singular"), "n/v sg": ("nominative", "singular"),
             "gen sg": ("genitive", "singular"), "dat sg": ("dative", "singular"),
             "acc sg": ("accusative", "singular"), "voc sg": ("vocative", "singular"),
             "nom pl": ("nominative", "plural"), "n/v pl": ("nominative", "plural"),
             "gen pl": ("genitive", "plural"), "dat pl": ("dative", "plural"),
             "acc pl": ("accusative", "plural")}
ROW_LABEL = re.compile(r"^(?:[123] (?:sg|pl)|(?:nom|gen|dat|acc|voc|n/v) (?:sg|pl))")
GREEK = re.compile(r"[Ͱ-Ͽἀ-῿]")
EMPTY = "—"


def _cell(line):
    """A grid cell - a Greek form, or a dash for an empty one - or None for a heading. The athematic
    charts print a stem after the lexical form, ἵστημι (*στα), which is dropped."""
    if set(line) <= set("—–-"):
        return EMPTY
    if not GREEK.search(line) or re.search(r"[A-Za-z0-9]", line):
        return None
    line = re.sub(r"\s*\(\*[^)]*\)", "", line)
    return re.sub(r"\s+\(ν\)", "(ν)", line).split(" / ")[0].strip()


def _grids(lines, start, end):
    """Every labelled grid between two lines, in order, as {row label: [cells]}. A grid ends at a
    heading, or where a row label comes round again."""
    grids, grid, row = [], None, None
    for line in lines[start:end]:
        label = ROW_LABEL.match(line)
        if label:
            if grid is None or label.group(0) in grid:
                grid = {}
                grids.append(grid)
            row = grid.setdefault(label.group(0), [])
        elif line:
            cell = _cell(line)
            if cell is None:
                grid = row = None
            elif row is not None:
                row.append(cell)
    return grids


def _infinitive_rows(lines, start, end):
    """The infinitive chart labels its rows with a heading rather than a row label, so it is read
    as {(Thematic|Athematic, heading): [cells]}. The morpheme chart printed between the two halves
    holds endings, not forms, and is passed over."""
    rows, half, heading = {}, None, None
    for line in lines[start:end]:
        if not line:
            continue
        cell = _cell(line)
        if cell is None:
            if line in ("Thematic", "Athematic"):
                half, heading = line, None
            elif line == "Infinitive Morpheme Chart":
                half = None
            else:
                heading = line
        elif half and heading:
            rows.setdefault((half, heading), []).append(cell)
    return rows


def _verb(lemma, stem):
    return lemma, stem


LU, POREUOMAI = _verb("λύω", "thematic"), _verb("πορεύομαι", "thematic")
GENNAO, POIEO, PHANEROO = (_verb("γεννάω", "contract -άω"), _verb("ποιέω", "contract -έω"),
                           _verb("φανερόω", "contract -όω"))
HISTEMI, TITHEMI, DIDOMI, DEIKNUMI = (_verb("ἵστημι", "athematic"), _verb("τίθημι", "athematic"),
                                      _verb("δίδωμι", "athematic"), _verb("δείκνυμι", "athematic"))
MENO, BALLO, GRAPHO = _verb("μένω", "liquid"), _verb("βάλλω", "second aorist"), _verb("γράφω", "second aorist")
GINOMAI = _verb("γίνομαι", "second aorist")
HISTEMI_1AOR = _verb("ἵστημι", "first aorist")
TITHEMI_K, DIDOMI_K = _verb("τίθημι", "κ-aorist"), _verb("δίδωμι", "κ-aorist")
HISTEMI_ROOT, TITHEMI_ROOT, DIDOMI_ROOT = (_verb("ἵστημι", "root aorist"), _verb("τίθημι", "root aorist"),
                                           _verb("δίδωμι", "root aorist"))
GINOMAI_PERF, HISTEMI_PERF = _verb("γίνομαι", "second perfect"), _verb("ἵστημι", "second perfect")
EIMI = _verb("εἰμί", "irregular")
GENDERS = ("masculine", "feminine", "neuter")


def _columns(rules, *verbs):
    return [(rules, verb, None) for verb in verbs]


def _genders(rules, verb, genders=GENDERS):
    return [(rules, verb, gender) for gender in genders]


def _mp(tense, mood):
    """A chart's one middle/passive column. The present, imperfect and perfect spell the middle and
    passive alike, so the two are one rule."""
    return [f"{tense}-midpas-{mood}"]


# One entry per grid, in the order the appendix prints them from "Indicative (MBG §40)" on; None
# for a grid not carried (the perfect imperatives) or a column not carried. A column is
# (rules it fills, (lemma, stem class), gender for a participle).
APPENDIX_VERBS = [
    _columns(["pres-act-ind"], LU, GENNAO, POIEO, PHANEROO),
    _columns(_mp("pres", "ind"), LU, GENNAO, POIEO, PHANEROO),
    _columns(["pres-act-ind"], HISTEMI, TITHEMI, DIDOMI, DEIKNUMI),
    _columns(_mp("pres", "ind"), HISTEMI, TITHEMI, DIDOMI, DEIKNUMI),
    _columns(["impf-act-ind"], LU, GENNAO, POIEO, PHANEROO),
    _columns(_mp("impf", "ind"), LU, GENNAO, POIEO, PHANEROO),
    _columns(["impf-act-ind"], HISTEMI, TITHEMI, DIDOMI, DEIKNUMI),
    _columns(_mp("impf", "ind"), HISTEMI, TITHEMI, DIDOMI, DEIKNUMI),
    _columns(["fut-act-ind"], LU, MENO, HISTEMI, TITHEMI, DIDOMI),
    _columns(["fut-mid-ind"], POREUOMAI, MENO, HISTEMI, TITHEMI, DIDOMI),
    _columns(["aor1-act-ind"], LU, MENO) + _columns(["aor2-act-ind"], BALLO)
    + _columns(["aor1-act-ind"], HISTEMI_1AOR, TITHEMI_K, DIDOMI_K),
    # the fourth column repeats, without its first persons, what the next grid prints whole
    _columns(["aor1-mid-ind"], LU, MENO) + _columns(["aor2-mid-ind"], GINOMAI) + [None],
    _columns(["aor2-act-ind"], HISTEMI_ROOT, TITHEMI_ROOT, DIDOMI_ROOT)
    + _columns(["aor2-mid-ind"], HISTEMI_ROOT, TITHEMI_ROOT, DIDOMI_ROOT),
    _columns(["perf-act-ind"], LU, GINOMAI_PERF, HISTEMI) + _columns(_mp("perf", "ind"), LU, TITHEMI, DIDOMI),
    _columns(["aor1-pas-ind"], LU) + _columns(["aor2-pas-ind"], GRAPHO)
    + _columns(["aor1-pas-ind"], HISTEMI, TITHEMI, DIDOMI),
    _columns(["fut-pas-ind"], LU, GRAPHO, HISTEMI, TITHEMI, DIDOMI),
    _columns(["pres-act-subj"], LU, GENNAO, POIEO, PHANEROO),
    _columns(_mp("pres", "subj"), LU, GENNAO, POIEO, PHANEROO),
    _columns(["aor1-act-subj"], LU),
    _columns(["aor1-mid-subj"], LU),
    _columns(["aor1-pas-subj"], LU),
    _columns(["pres-act-subj"], HISTEMI, TITHEMI, DIDOMI),
    _columns(_mp("pres", "subj"), HISTEMI, TITHEMI, DIDOMI),
    _columns(["aor2-act-subj"], HISTEMI_ROOT, TITHEMI_ROOT, DIDOMI_ROOT),
    _columns(["aor2-mid-subj"], HISTEMI_ROOT, TITHEMI_ROOT, DIDOMI_ROOT),
    _columns(["pres-act-impv"], LU, GENNAO, POIEO, PHANEROO),
    _columns(_mp("pres", "impv"), LU, GENNAO, POIEO, PHANEROO),
    _columns(["aor1-act-impv"], LU) + _columns(["aor2-act-impv"], BALLO),
    _columns(["aor1-mid-impv"], LU) + _columns(["aor2-mid-impv"], GINOMAI),
    _columns(["aor1-pas-impv"], LU, GENNAO, POIEO, PHANEROO),
    None,
    None,
    _columns(["pres-act-impv"], HISTEMI, TITHEMI, DIDOMI, DEIKNUMI),
    _columns(_mp("pres", "impv"), HISTEMI, TITHEMI, DIDOMI, DEIKNUMI),
    _columns(["aor2-act-impv"], HISTEMI_ROOT, TITHEMI_ROOT, DIDOMI_ROOT),
    _columns(["aor2-mid-impv"], HISTEMI_ROOT, TITHEMI_ROOT, DIDOMI_ROOT),
    # Participle (MBG §90), thematic
    _genders(["pres-act-ptc"], LU),
    _genders(_mp("pres", "ptc"), LU),
    _genders(["aor1-act-ptc"], LU) + _genders(["aor2-act-ptc"], BALLO),
    _genders(["aor1-mid-ptc"], LU) + _genders(["aor2-mid-ptc"], BALLO),
    _genders(["aor1-pas-ptc"], LU) + _genders(["aor2-pas-ptc"], GRAPHO),
    _genders(["perf-act-ptc"], LU),
    _genders(_mp("perf", "ptc"), LU),
    # athematic: nominative and genitive singular only, one grid per verb
    *[_genders(["pres-act-ptc"], verb) for verb in (HISTEMI, TITHEMI, DIDOMI, DEIKNUMI)],
    *[_genders(_mp("pres", "ptc"), verb) for verb in (HISTEMI, TITHEMI, DIDOMI, DEIKNUMI)],
    _genders(["aor1-act-ptc"], HISTEMI_1AOR) + _genders(["aor2-act-ptc"], HISTEMI_ROOT),
    _genders(["aor1-act-ptc"], TITHEMI_K) + _genders(["aor2-act-ptc"], TITHEMI_ROOT),
    [None, None, None] + _genders(["aor2-act-ptc"], DIDOMI_ROOT),
    _genders(["aor1-mid-ptc"], HISTEMI_1AOR) + _genders(["aor2-mid-ptc"], HISTEMI_ROOT),
    _genders(["aor1-mid-ptc"], TITHEMI_K) + _genders(["aor2-mid-ptc"], TITHEMI_ROOT),
    _genders(["aor2-mid-ptc"], DIDOMI_ROOT),
    *[_genders(["aor1-pas-ptc"], verb) for verb in (HISTEMI, TITHEMI, DIDOMI)],
    [(["perf-act-ptc"], HISTEMI, "masculine")] + _genders(["perf-act-ptc"], HISTEMI_PERF),
    [(["perf-act-ptc"], TITHEMI, "masculine")],
    [(["perf-act-ptc"], DIDOMI, "masculine")],
    *[_genders(_mp("perf", "ptc"), verb) for verb in (HISTEMI, TITHEMI, DIDOMI)],
]

# The infinitive rows, by (half, heading). Rows not listed are not carried: the aorist middle's
# μενεῖσθαι is a future, and the athematic perfect middle/passive row holds only ἑστάναι, an active.
APPENDIX_INFINITIVES = {
    ("Thematic", "present active"): _columns(["pres-act-inf"], LU, MENO, GENNAO, POIEO, PHANEROO),
    ("Thematic", "present middle passive"): _columns(_mp("pres", "inf"), LU, MENO, GENNAO, POIEO, PHANEROO),
    ("Thematic", "aorist active"): _columns(["aor1-act-inf"], LU) + _columns(["aor2-act-inf"], BALLO)
    + _columns(["aor1-act-inf"], MENO, GENNAO, POIEO, PHANEROO),
    ("Thematic", "aorist middle"): _columns(["aor1-mid-inf"], LU) + [None]
    + _columns(["aor1-mid-inf"], GENNAO, POIEO, PHANEROO),
    ("Thematic", "aorist passive"): _columns(["aor1-pas-inf"], LU) + _columns(["aor2-pas-inf"], GRAPHO)
    + _columns(["aor1-pas-inf"], GENNAO, POIEO, PHANEROO),
    ("Thematic", "perfect active"): _columns(["perf-act-inf"], LU, GINOMAI_PERF, GENNAO, POIEO, PHANEROO),
    ("Thematic", "perfect middle/passive"): _columns(_mp("perf", "inf"), LU, GENNAO, POIEO, PHANEROO),
    ("Athematic", "present active"): _columns(["pres-act-inf"], HISTEMI, TITHEMI, DIDOMI, DEIKNUMI)
    + _columns(["eimi-pres-inf"], EIMI),
    ("Athematic", "present middle passive"): _columns(_mp("pres", "inf"), HISTEMI, TITHEMI, DIDOMI),
    ("Athematic", "aorist active"): _columns(["aor1-act-inf"], HISTEMI_1AOR)
    + _columns(["aor2-act-inf"], HISTEMI_ROOT, TITHEMI_ROOT, DIDOMI_ROOT),
    ("Athematic", "aorist middle"): _columns(["aor1-mid-inf"], HISTEMI_1AOR)
    + _columns(["aor2-mid-inf"], HISTEMI_ROOT, TITHEMI_ROOT, DIDOMI_ROOT),
    ("Athematic", "aorist passive"): _columns(["aor1-pas-inf"], HISTEMI, TITHEMI, DIDOMI),
    ("Athematic", "perfect active"): _columns(["perf-act-inf"], HISTEMI, TITHEMI, DIDOMI),
}


def _nominal(rule, pattern, genders=(None,)):
    return [(rule, gender, pattern) for gender in genders]


def _nouns(rule, *codes):
    return [(rule, None, code) for code in codes]


# The declension, adjective and pronoun grids from "First Declension Nouns" on. A column is
# (rule, gender, pattern); nouns carry no gender in their keys, and a masc & fem column carries none
# either. The pattern is the MBG code the appendix prints over the column. BBGG prints one code, a-1a,
# over both 2-1-2 adjectives, whose feminines differ, so they are told apart by the feminine's vowel.
# A pronoun, the article and the irregular adjectives are each their own pattern, named by the word.
# The article and relative pronoun printed beside the first declension come from GrammarSummaries.
APPENDIX_NOMINALS = [
    _nouns("decl1", "n-1a", "n-1b", "n-1c", "n-1d") + [None] * 3,
    _nouns("decl1", "n-1e", "n-1f", "n-1g", "n-1h") + [None] * 3,
    _nouns("decl2", "n-2a", "n-2b", "n-2c", "n-2d(1)", "n-2d(2)", "n-2e"),
    _nouns("decl3", "n-3b(1)", "n-3b(1)", "n-3b(3)", "n-3c(1)", "n-3c(2)", "n-3c(4)"),
    _nouns("decl3", "n-3c(5b)", "n-3c(6a)", "n-3c(6b)", "n-3c(6c)", "n-3d(2a)", "n-3d(2b)"),
    _nouns("decl3", "n-3e(1)", "n-3e(3)", "n-3e(4)", "n-3e(5b)", "n-3f(1a)", "n-3f(1b)"),
    _nouns("decl3", "n-3f(2a)", "n-3f(2b)", "n-3f(2c)", "n-3f(2c)", "n-3f(2c)", "n-3f(2c)"),
    _nominal("adjective-2-1-2", "a-1a(α)", GENDERS) + _nominal("adjective-2-1-2", "a-1a(η)", GENDERS),
    _nominal("pronoun-demonstrative", "οὗτος", GENDERS) + _nominal("adjective-irregular", "μέγας", GENDERS),
    _nominal("adjective-irregular", "πολύς", GENDERS) + _nominal("pronoun-indefinite-relative", "ὅστις", GENDERS),
    _nominal("adjective-3-1-3", "a-2a", GENDERS) + _nominal("adjective-3-1-3", "a-2b", GENDERS),
    _nominal("adjective-2-2", "a-3a", (None, "neuter")) + _nominal("adjective-3-3", "a-4a", (None, "neuter"))
    + _nominal("pronoun-personal", "αὐτός", GENDERS),
    _nominal("adjective-3-3", "a-4b(1)", (None, "neuter")) * 2,
    _nominal("pronoun-interrogative", "τίς", (None, "neuter")) + _nominal("pronoun-indefinite", "τις", (None, "neuter"))
    + _nominal("numeral", "εἷς", GENDERS),
]

# Cells the appendix has wrong, by (rule, lemma, slot). Each is a dropped letter, a doubled
# ending, or a form printed in the wrong row; the corrected form is the one the parallel columns
# and the grammars' own rules give.
CORRECTIONS = {
    ("pres-midpas-ind", "φανερόω", ("third_person", "plural")): "φανεροῦνται",
    ("fut-act-ind", "τίθημι", ("third_person", "plural")): "θήσουσι(ν)",
    ("aor1-act-ind", "ἵστημι", ("third_person", "plural")): "ἔστησαν",
    ("aor1-pas-ind", "ἵστημι", ("third_person", "singular")): "ἐστάθη",
    ("aor2-act-subj", "ἵστημι", ("second_person", "plural")): "στῆτε",
}

TENSE_KEYS = {"pres": "present", "impf": "imperfect", "fut": "future", "aor1": "aorist",
              "aor2": "aorist", "perf": "perfect"}
MOOD_KEYS = {short: mood for mood, short in MOODS.items()}


def _rule_identity(rule):
    """tense key, tense, voice and mood from a rule key such as aor1-pas-ptc or eimi-pres-subj."""
    parts = rule.split("-")
    if parts[0] == "eimi":
        return parts[1], TENSE_KEYS[parts[1]], "act", MOOD_KEYS[parts[2]]
    return parts[0], TENSE_KEYS[parts[0]], parts[1], MOOD_KEYS[parts[2]]


def _index_of(lines, text, after=0):
    return next(index for index in range(after, len(lines)) if lines[index] == text)


def _paradigm(rule, verb, gender, slots, chart, corrected):
    lemma, stem = verb
    fixed = {}
    for slot, form in slots.items():
        fix = CORRECTIONS.get((rule, lemma, slot))
        if fix and fix != form:
            corrected.append({"rule": rule, "lemma": lemma, "slot": list(slot), "printed": form,
                              "corrected": fix})
            form = fix
        fixed[slot] = form
    tense_key, tense, voice, mood = _rule_identity(rule)
    return {"rule": rule, "tense": tense, "voice": voice, "mood": mood, "slots": fixed,
            "lexical_form": next(iter(fixed.values())), "lemma": lemma, "stem_class": stem,
            "gender": gender, "chart": chart}


def _appendix_verbs(lines, corrected):
    """Every verb paradigm the appendix prints beyond the Overviews, with εἰμί's non-indicative
    forms and participle, which are printed just before them."""
    start = _index_of(lines, "non-indicative")
    mbg = _index_of(lines, "Indicative (MBG §40)", start)
    infinitive = _index_of(lines, "Infinitive (MBG §80)", mbg)
    participle = _index_of(lines, "Participle (MBG §90)", infinitive)
    end = _index_of(lines, "Tense Forms of Verbs Occurring Fifty Times or More", participle)
    grids = _grids(lines, start, end)
    if len(grids) != 2 + len(APPENDIX_VERBS):
        raise ValueError(f"appendix verb grids: found {len(grids)}, declared {2 + len(APPENDIX_VERBS)}")

    paradigms = []
    eimi, eimi_participle = grids[0], grids[1]
    paradigms.append(_paradigm("eimi-pres-subj", EIMI, None,
                               {ROW_SLOTS[label]: cells[0] for label, cells in eimi.items()},
                               "εἰμί (non-indicative)", corrected))
    paradigms.append(_paradigm("eimi-pres-impv", EIMI, None,
                               {ROW_SLOTS[label]: cells[1] for label, cells in eimi.items()
                                if label not in ("1 sg", "1 pl") and len(cells) > 1},
                               "εἰμί (non-indicative)", corrected))
    grids = [eimi_participle] + grids[2:]
    declared = [_genders(["eimi-pres-ptc"], EIMI)] + APPENDIX_VERBS
    for grid, columns in zip(grids, declared):
        for index, column in enumerate(columns or []):
            if column is None:
                continue
            rules, verb, gender = column
            slots = {ROW_SLOTS[label]: cells[index] for label, cells in grid.items()
                     if index < len(cells) and cells[index] != EMPTY}
            for rule in rules:
                if slots:
                    paradigms.append(_paradigm(rule, verb, gender, slots, "Appendix (MBG)", corrected))

    for (half, heading), cells in _infinitive_rows(lines, infinitive, participle).items():
        for index, column in enumerate(APPENDIX_INFINITIVES.get((half, heading), [])):
            if column is None or index >= len(cells) or cells[index] == EMPTY:
                continue
            rules, verb, _ = column
            for rule in rules:
                paradigms.append(_paradigm(rule, verb, None, {"_": cells[index]},
                                           "Infinitive (MBG §80)", corrected))
    return paradigms


def _appendix_nominals(lines):
    """The declension, adjective and pronoun grids, as case paradigms."""
    end = _index_of(lines, "a-5", _index_of(lines, "The Eight Noun Rules"))
    start = max(index for index in range(end) if lines[index] == "First Declension Nouns")
    grids = _grids(lines, start, end)
    if len(grids) != len(APPENDIX_NOMINALS):
        raise ValueError(f"appendix nominal grids: found {len(grids)}, declared {len(APPENDIX_NOMINALS)}")
    found = []
    for grid, columns in zip(grids, APPENDIX_NOMINALS):
        for index, column in enumerate(columns):
            if column is None:
                continue
            rule, gender, pattern = column
            slots = {ROW_SLOTS[label]: cells[index] for label, cells in grid.items()
                     if index < len(cells) and cells[index] != EMPTY}
            found.append({"resource": "BBGG", "section": "Appendix", "rule": rule, "gender": gender,
                          "pattern": pattern, "lexical_form": next(iter(slots.values())), "page": None,
                          "slots": slots})
    return found


def _case_paradigms():
    """The article, relative and personal pronouns, and the declensions, from GrammarSummaries'
    charts in the builder's typed output. BBGG's appendix supplies everything else, and where both
    print a paradigm BBGG's is kept, since it carries the vocative.

    These already carry CASE_NUMBER_SLOTS, so unlike the verb charts they need no
    reinterpretation - only a rule name and a filter for the ones printing bare endings."""
    found = []
    for resource in ("GrammarSummaries",):
        path = BUILDER / "data" / resource / "paradigms.json"
        if not path.exists():
            continue
        for chart in json.loads(path.read_text(encoding="utf-8")):
            for paradigm in chart["paradigms"]:
                if paradigm["slot_order"] != "CASE_NUMBER_SLOTS" or paradigm["cells"] != "forms":
                    continue
                forms = paradigm["morphological_forms"]
                if len(forms) != len(CASE_NUMBER):
                    continue
                found.append({
                    "resource": resource, "section": chart["section"],
                    "lexical_form": paradigm["lexical_form"],
                    "page": chart["source"]["page"],
                    "slots": dict(zip(CASE_NUMBER, forms)),
                })
    return found


# Chart section names mapped onto rule names. Book knowledge, so it is data - and it is a handful
# of strings rather than a rule engine. Anything unlisted is slugified from its section.
CASE_RULES = {
    "Definite Article": "article",
    "First and Second Declension Nouns": "decl1-decl2",
    "Third Declension": "decl3",
    "Case Endings and Rules": "case-endings",
    "Personal Pronouns": "pronoun-personal",
}
RULE_NAMES = {
    "article": "Definite Article", "pronoun-relative": "Relative Pronoun",
    "decl1": "First Declension Nouns", "decl2": "Second Declension Nouns",
    "decl3": "Third Declension Nouns", "pronoun-personal": "Personal Pronouns",
    "pronoun-demonstrative": "Demonstrative Pronoun", "pronoun-interrogative": "Interrogative Pronoun",
    "pronoun-indefinite": "Indefinite Pronoun", "pronoun-indefinite-relative": "Indefinite Relative Pronoun",
    "adjective-2-1-2": "Adjectives (2-1-2)", "adjective-2-2": "Adjectives (2-2)",
    "adjective-3-1-3": "Adjectives (3-1-3)", "adjective-3-3": "Adjectives (3-3)",
    "adjective-irregular": "Irregular Adjectives (μέγας, πολύς)", "numeral": "Numeral εἷς",
}
# The Overviews print their second-aorist column on a different verb for each voice.
OVERVIEW_LEMMAS = {("aor2", "act"): "λαμβάνω", ("aor2", "mid"): "γίνομαι", ("aor2", "pas"): "γράφω"}
VOICE_NAMES = {"act": "Active", "mid": "Middle", "pas": "Passive", "midpas": "Middle/Passive"}
# Features and parsing strings spell the voice out; only the rule key is abbreviated.
VOICE_FULL = {"act": "active", "mid": "middle", "pas": "passive",
              "midpas": "middle/passive"}

# Two charts each hold more than one rule. GrammarSummaries prints the article and the relative
# pronoun under one heading - they decline alike, which is the point of printing them together -
# and its declension chart covers the first and second together. Splitting them by lexeme keeps
# the rule names meaning what they say.
LEXEME_RULES = {
    "ὁ": "article", "ἡ": "article", "τό": "article",
    "ὅς": "pronoun-relative", "ἥ": "pronoun-relative", "ὅ": "pronoun-relative",
    "ὥρα": "decl1", "γραφή": "decl1", "δόξα": "decl1", "προφήτης": "decl1",
    "λόγος": "decl2", "ἔργον": "decl2",
    # GrammarSummaries prints these under "Personal Pronouns"
    "οὗτος": "pronoun-demonstrative", "αὕτη": "pronoun-demonstrative", "τοῦτο": "pronoun-demonstrative",
    "τίς": "pronoun-interrogative", "τί": "pronoun-interrogative",
    "ὅστις": "pronoun-indefinite-relative", "ἥτις": "pronoun-indefinite-relative",
    "ὅτι": "pronoun-indefinite-relative",
}

# Charts that print one gender per column give a separate chart per gender, so the gender is
# carried by the lexeme rather than by a column header.
GENDER_BY_LEXEME = {
    "ὁ": "masculine", "ἡ": "feminine", "τό": "neuter",
    "ὅς": "masculine", "ἥ": "feminine", "ὅ": "neuter",
    "αὐτός": "masculine", "αὐτή": "feminine", "αὐτό": "neuter",
    "οὗτος": "masculine", "αὕτη": "feminine", "τοῦτο": "neuter",
    "ἐκεῖνος": "masculine", "ἐκείνη": "feminine", "ἐκεῖνο": "neuter",
}
# GrammarSummaries' charts that BBGG's appendix does not print, by the pattern each belongs to.
SUMMARY_PATTERNS = {"ὁ": "ὁ", "ἡ": "ὁ", "τό": "ὁ", "ὅς": "ὅς", "ἥ": "ὅς", "ὅ": "ὅς", "ἐγώ": "ἐγώ", "σύ": "σύ"}
TENSE_NAMES = {"pres": "Present", "impf": "Imperfect", "fut": "Future", "perf": "Perfect",
               "aor1": "First Aorist", "aor2": "Second Aorist"}
MOOD_NAMES = {"indicative": "Indicative", "subjunctive": "Subjunctive",
              "imperative": "Imperative", "infinitive": "Infinitive", "participle": "Participle"}

# A verb chart's stem class, as the derivation reads it from the chart's heading, and the pattern it
# files under. ἵστημι's first aorist is printed as "first aorist athematic".
PATTERN_OF_STEM = {
    "thematic": "thematic", "contract -άω": "contract-άω", "contract -έω": "contract-έω",
    "contract -όω": "contract-όω", "liquid": "liquid", "athematic": "athematic", "first aorist": "athematic",
    "κ-aorist": "κ-aorist", "second aorist": "second-aorist", "root aorist": "root-aorist",
    "second perfect": "second-perfect", "irregular": "εἰμί",
}
VERB_PATTERN_NAMES = {
    "thematic": "Thematic", "contract-άω": "Thematic contracted, -άω", "contract-έω": "Thematic contracted, -έω",
    "contract-όω": "Thematic contracted, -όω", "liquid": "Liquid", "athematic": "Athematic",
    "κ-aorist": "Athematic κ-aorist", "second-aorist": "Second aorist", "root-aorist": "Athematic second aorist",
    "second-perfect": "Second perfect", "εἰμί": "εἰμί",
}


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40]


def _merged(rule):
    """The present, imperfect and perfect middle and passive are one rule."""
    tense, voice, mood = rule.split("-")
    return f"{tense}-midpas-{mood}" if tense in ("pres", "impf", "perf") and voice in ("mid", "pas") else rule


def _verb_rules(lines):
    """Every verb paradigm BBGG's appendix prints, keyed by rule."""
    starts = {}
    for index, line in enumerate(lines):
        for title, _, _ in OVERVIEWS:
            if line == title:
                starts[title] = index
    rules = {}
    for title, mood, row_labels in OVERVIEWS:
        if title not in starts:
            continue
        charts, _ = _read_overview(lines, starts[title], mood, row_labels)
        for (tense_key, tense, voice), slots in charts.items():
            rule = f"{tense_key}-{voice}-{MOODS[mood]}"
            lead = slots.get(("first_person", "singular")) or slots.get(
                ("second_person", "singular")) or next(iter(slots.values()))
            rules[rule] = {"tense": tense, "voice": voice, "mood": mood, "slots": slots,
                           "lexical_form": lead, "chart": title}
    if "Overview of Infinitive" in starts:
        for (tense_key, tense, voice), slots in _eimi(
                lines, starts["Overview of Infinitive"] + 20).items():
            rules[f"eimi-{tense_key}-ind"] = {
                "tense": tense, "voice": "act", "mood": "indicative", "slots": slots,
                "lexical_form": "εἰμί", "chart": "Overview of Infinitive (εἰμί)"}
    return rules


def _describe(rule):
    tense_key, tense, voice, mood = _rule_identity(rule)
    if rule.startswith("eimi"):
        return (f"{TENSE_NAMES[tense_key]} {mood} of εἰμί. The verb is athematic and irregular, so its "
                f"forms are learned as a set rather than built from a rule.")
    return (f"{TENSE_NAMES[tense_key]} {VOICE_FULL[voice]} {mood}, as BBGG's appendix prints it on the "
            f"paradigm verb and, where it prints them, on contract, liquid and athematic verbs. "
            f"The forms are given whole rather than derived, which is how the charts state them.")


def _verb_charts(lines, corrected):
    """Every verb chart, the Overviews first, so where the appendix repeats λύω the Overview's stands."""
    charts = []
    for rule, spec in sorted(_verb_rules(lines).items()):
        tense_key = _rule_identity(rule)[0]
        lemma = "εἰμί" if rule.startswith("eimi") else OVERVIEW_LEMMAS.get((tense_key, spec["voice"]), "λύω")
        stem = "irregular" if lemma == "εἰμί" else "second aorist" if tense_key == "aor2" else "thematic"
        charts.append({**spec, "rule": _merged(rule), "lemma": lemma, "stem_class": stem, "gender": None})
    charts += _appendix_verbs(lines, corrected)
    for chart in charts:
        chart["pattern"] = PATTERN_OF_STEM[chart["stem_class"]]
        chart["source"] = {"resource": "BBGG", "chapter": "Appendix", "header": chart["chart"], "page": None}
    return charts


def _nominal_charts(lines):
    """Every declension, adjective, pronoun and article chart: BBGG's appendix, then the charts only
    GrammarSummaries prints. A chart's group is the set of gender columns printed for one word."""
    charts = _appendix_nominals(lines)
    printed = {(chart["rule"], chart["pattern"]) for chart in charts}
    for chart in _case_paradigms():
        rule = LEXEME_RULES.get(chart["lexical_form"], CASE_RULES.get(chart["section"], _slug(chart["section"])))
        pattern = SUMMARY_PATTERNS.get(chart["lexical_form"])
        if pattern and (rule, pattern) not in printed:
            charts.append({**chart, "rule": rule, "pattern": pattern,
                           "gender": GENDER_BY_LEXEME.get(chart["lexical_form"])})
    group = 0
    for index, chart in enumerate(charts):
        if index and (chart["gender"] in (None, "masculine") or chart["pattern"] != charts[index - 1]["pattern"]):
            group += 1
        chart["group"] = group
        chart["source"] = {"resource": chart["resource"], "chapter": "Appendix", "header": chart["section"],
                           "page": chart["page"]}
    return charts


# ---- the New Testament's forms ----------------------------------------------------------------

# A slot the GNT uses fewer times than MIN_OCCURRENCES across its rule, or than MIN_PATTERN_OCCURRENCES
# in its pattern, or only on words rarer than KNOWN_FREQUENCY (those a student has likely met by the
# intermediate level), is not an item: it is better met in reading than drilled. Each item carries
# up to GNT_FORMS of the GNT's own forms of it, one per word, known words first.
MIN_OCCURRENCES = 20
MIN_PATTERN_OCCURRENCES = 5
GNT_FORMS = 3
KNOWN_FREQUENCY = 20

PERSONS = {"p1": "first_person", "p2": "second_person", "p3": "third_person"}
PASSIVE_FORM = re.compile(r"θ(η|ω|ει|ε[ντ])")
# N1904 tags εὐθύς "immediately" as the adjective, so it would stand for a 3-1-3 form it is not.
NOT_NOMINAL = {"εὐθύς"}
TOKEN_TENSES = {"present": "pres", "imperfect": "impf", "future": "fut", "aorist": "aor", "perfect": "perf"}
TOKEN_VOICES = {"active": "act", "middle": "mid", "passive": "pas"}
FAMILIES = ("ιστημι", "τιθημι", "διδωμι", "δεικνυμι")
# Verbs whose other tenses are built on another root. Their forms outside the present system are
# real, but no pattern predicts them, so they come last.
SUPPLETIVE = ("λεγω", "ερχομαι", "οραω", "φερω", "εσθιω", "τρεχω", "αιρεω")
AORIST_ENDINGS = ("αμεθα", "ασθε", "αμην", "αμεν", "αντο", "ατε", "ατο", "αν", "ας", "εν", "α", "ε", "ω")
FUTURE_ENDINGS = ("ουμεθα", "ομεθα", "ουνται", "ονται", "εισθε", "εσθε", "ουμαι", "ομαι", "ειται", "εται",
                  "ουσιν", "ουσι", "ουμεν", "ομεν", "ειτε", "ετε", "εις", "ει", "η", "ω")


def _gnt_forms(api):
    """Every inflected word in N1904 that is not a name, counted by written form and analysis.

    N1904 tags a deponent's θη-aorist and θησ-future middle (ἀπεκρίθη); by form it is passive, and
    filed so. A comparative or superlative is filed under its own masculine nominative (μείζων), since
    it declines apart from its positive."""
    F = api.F
    counts = collections.Counter()
    for node in F.otype.s("word"):
        form, lemma = normalize_greek(F.normalized.v(node)), _lexical(F.lemma.v(node))
        if F.typems.v(node) == "proper" or not (F.case.v(node) or F.mood.v(node)) or "’" in form \
                or lemma in NOT_NOMINAL:
            continue
        form = form.lower() if lemma[:1].islower() else form
        voice, tense = F.voice.v(node), F.tense.v(node)
        if voice == "middle" and tense in ("aorist", "future") and PASSIVE_FORM.search(fold_greek(form)):
            voice = "passive"
        if F.degree.v(node):
            lemma = (lemma, F.degree.v(node))
        counts[(form, lemma, F.cls.v(node), tense, voice, F.mood.v(node), PERSONS.get(F.person.v(node)),
                F.case.v(node), F.gender.v(node), F.number.v(node),
                (F.morph.v(node) or "")[2:3] == "2")] += 1
    names = {}
    for key, count in counts.items():
        if isinstance(key[1], tuple) and key[7] == "nominative" and key[9] == "singular" and key[8] != "neuter":
            names.setdefault(key[1], collections.Counter())[key[0]] += count
    return collections.Counter({(key[0], names[key[1]].most_common(1)[0][0] if isinstance(key[1], tuple) else key[1],
                                 *key[2:]): count
                                for key, count in counts.items()
                                if not isinstance(key[1], tuple) or key[1] in names})


def _lexical(text):
    """A lemma without the grave accent N1904 writes on some (τὶς), so it compares with the charts."""
    return normalize_greek("".join(c for c in unicodedata.normalize("NFD", text) if c != "\u0300"))


def _family(folded):
    return next((family for family in FAMILIES if folded.endswith(family)), None)


def _liquid_verbs(forms):
    """(lemma, tense) pairs whose aorist or future indicative puts a liquid where other verbs put σ:
    the liquid verbs, found by what they do rather than listed."""
    tally = collections.defaultdict(collections.Counter)
    for (form, lemma, _, tense, voice, mood, *_, two), count in forms.items():
        endings = {"aorist": AORIST_ENDINGS, "future": FUTURE_ENDINGS}.get(tense)
        if mood != "indicative" or voice not in ("active", "middle") or two or not endings:
            continue
        folded = fold_greek(form)
        ending = next((ending for ending in endings if folded.endswith(ending)), None)
        if ending and len(folded) > len(ending):
            tally[(lemma, "aor1" if tense == "aorist" else "fut")][folded[-len(ending) - 1] in "λμνρ"] += count
    return {key for key, sides in tally.items() if sides[True] > sides[False]}


def _verb_slot(lemma, tense, voice, mood, person, case, gender, number, two):
    """The rule and slot fragment a GNT verb form fills, or None."""
    if tense not in TOKEN_TENSES or mood not in MOODS:
        return None
    tense = TOKEN_TENSES[tense]
    if lemma == "εἰμί":
        rule = f"eimi-{tense}-{MOODS[mood]}"
    else:
        tense = ("aor2" if two else "aor1") if tense == "aor" else tense
        voice = "act" if voice == "active" else "midpas" if tense in ("pres", "impf", "perf") \
            else TOKEN_VOICES.get(voice)
        if not voice:
            return None
        rule = f"{tense}-{voice}-{MOODS[mood]}"
    fragment = (case, gender, number) if mood == "participle" else (person, number) if person else ()
    return rule, ".".join(fragment)


def _verb_pattern(lemma, rule, two, liquid):
    """The pattern a GNT verb form belongs to within its rule, and its athematic family if it has
    one. None for a verb no chart covers (ἀφίημι, δύναμαι, κεῖμαι)."""
    folded = fold_greek(lemma)
    tense, voice = rule.split("-")[:2]
    family = _family(folded)
    if lemma == "εἰμί":
        return "εἰμί", None
    if family:
        if two:
            return ("root-aorist" if tense == "aor2" else "second-perfect"), family
        kappa = tense == "aor1" and voice == "act" and family in ("τιθημι", "διδωμι")
        return ("κ-aorist" if kappa else "athematic"), family
    if not folded.endswith(("ω", "ομαι")) or folded.endswith("μι") or folded.endswith("μαι") and \
            not folded.endswith("ομαι"):
        return None, None    # an athematic verb no chart covers, or a lemma that is no verb's (δεῖ, οἶδα, εἶπον)
    if two:
        return ("second-perfect" if tense == "perf" else "second-aorist"), None
    if tense in ("pres", "impf"):
        vowel = next((vowel for vowel in "αεο" if folded.endswith((vowel + "ω", vowel + "ομαι"))), None)
        return ({"α": "contract-άω", "ε": "contract-έω", "ο": "contract-όω"}[vowel] if vowel else "thematic"), None
    if tense in ("fut", "aor1") and voice in ("act", "mid"):
        return ("liquid" if (lemma, tense) in liquid else "thematic"), None
    return "thematic", None


def _bare(cell):
    """A chart cell as compared: its first spelling folded, and whether it prints a movable ν."""
    first = cell.split(",")[0].strip()
    return fold_greek(first.replace("(ν)", "")), "(ν)" in first


FORMANTS = {"σ": "σψξ", "θ": "θ", "κ": "κ"}


def _chart_endings(chart, siblings):
    """Each cell's ending - what follows the letters all the chart's cells share - with the tense
    formant (σ, θ, κ) it must follow. A chart of one cell (an infinitive) is read against its verb's
    other charts in the same tense and voice, and failing those is held to its last two letters."""
    bare = {slot: _bare(cell) for slot, cell in chart["slots"].items()}
    texts = [text for text, _ in bare.values()]
    if len(texts) == 1:
        texts += [_bare(cell)[0] for other in siblings for cell in other["slots"].values()]
    prefix = os.path.commonprefix(texts) if len(texts) > 1 else ""
    if any(text == prefix for text in texts):
        prefix = prefix[:-1]
    if len(prefix) < 2:
        return {slot: (text[-2:], movable, None) for slot, (text, movable) in bare.items()}
    formant = None if chart["pattern"].startswith(("second", "root")) else FORMANTS.get(prefix[-1])
    return {slot: (text[len(prefix):], movable, formant) for slot, (text, movable) in bare.items()}


def _ends_like(form, ending, movable, formant):
    folded = fold_greek(form)
    for text in ({folded, folded[:-1]} if movable and folded.endswith("ν") else {folded}):
        if text.endswith(ending) and (not formant or text[-len(ending) - 1:-len(ending) or None][:1] in formant):
            return True
    return False


def _is(form, text, movable):
    """Whether a form is a chart's text, a movable ν either way."""
    folded = fold_greek(form)
    return text in ({folded, folded[:-1]} if movable and folded.endswith("ν") else {folded})


def _chart_gender(charts, gender):
    """The gender column a nominal form reads from: none for a noun, whose gender is its own; the
    common masculine-and-feminine column where the charts print one; False where none prints it."""
    genders = {chart["gender"] for chart in charts}
    if charts[0]["rule"].startswith("decl"):
        return None
    if gender in genders:
        return gender
    return None if None in genders and gender != "neuter" else False


def _nominal_fit(charts, lemma, tokens, gender):
    """How well a word declines as a group of charts does, or None where it does not: nine in ten of
    its forms in the charts' slots are the charts' ending on one stem, its lemma included, and a noun
    shares the charts' gender. A fit ranks by the forms it explains, then by how much of the word the
    endings pin down, then by how many slots the charts print."""
    bare = {(slot, chart["gender"]): _bare(cell) for chart in charts for slot, cell in chart["slots"].items()}
    prefix = os.path.commonprefix([text for text, _ in bare.values()])
    if any(text == prefix for text, _ in bare.values()):
        prefix = prefix[:-1]    # keep the theme vowel every form shares (σατανᾶ-, κῶ-) in the endings
    lead = charts[0]
    nominative = bare.get((("nominative", "singular"), lead["gender"]))
    folded = fold_greek(lemma)
    if nominative is None or not folded.endswith(nominative[0][len(prefix):]):
        return None
    if lead["rule"].startswith("decl") and lead["lemma_gender"] and gender != lead["lemma_gender"]:
        return None
    stem = folded[:len(folded) - len(nominative[0]) + len(prefix)]
    matched, total, slots = 0, 0, set()
    for form, slot, form_gender, count in tokens:
        key = (slot, _chart_gender(charts, form_gender))
        if key not in bare:
            continue
        text, movable = bare[key]
        total += count
        if _is(form, stem + text[len(prefix):], movable):
            matched += count
            slots.add(key)
    if total and matched / total >= 0.9 and len(slots) >= 2:
        return matched, len(nominative[0]) - len(prefix), len(bare)
    return None


def _best_group(lemma, scores, groups):
    """The group a word is filed under. A chart's own word goes to its chart; otherwise the best fit,
    and among fits equally good, the chart whose stem ends as the word's does (ε, ι, ρ or not: the
    grammars' rule for a feminine in α), then the one printed first."""
    def stem_class(text):
        return fold_greek(text).rstrip("σνς")[-2:-1] in "ειρ"
    for group in scores:
        if groups[group][0]["lexical_form"] == lemma:
            return group
    best = max(scores.values())
    tied = [group for group, score in scores.items() if score == best]
    return min(tied, key=lambda group: (stem_class(groups[group][0]["lexical_form"]) != stem_class(lemma), group))


def _ranked(candidates, lemma_counts, irregular, word):
    """Up to GNT_FORMS of the GNT's forms for one item. For a pronoun or the article, its commonest
    spellings; otherwise one form per word a student likely knows, regular forms first, commonest
    first."""
    if word:
        spellings = collections.Counter()
        for (form, lemma), count in candidates.items():
            spellings[fold_greek(form)] += count
        commonest = {}
        for (form, lemma), count in candidates.most_common():
            commonest.setdefault(fold_greek(form), (form, lemma))
        return [{"form": commonest[text][0], "lemma": commonest[text][1], "occurrences": count}
                for text, count in spellings.most_common(GNT_FORMS)]
    best = {}
    for (form, lemma), count in candidates.most_common():
        if lemma_counts[lemma] >= KNOWN_FREQUENCY:
            best.setdefault(lemma, (form, count))
    order = sorted(best.items(), key=lambda entry: (entry[0] in irregular, -entry[1][1]))
    return [{"form": form, "lemma": lemma, "occurrences": count} for lemma, (form, count) in order[:GNT_FORMS]]


# ---- the scaffolding -------------------------------------------------------------------------

def _fragment(slot, gender=None):
    if not isinstance(slot, tuple):
        return ""
    if len(slot) == 2 and slot[0] in CASES:
        return ".".join(filter(None, (slot[0], gender, slot[1])))
    return ".".join(slot)


CASES = ("nominative", "genitive", "dative", "accusative", "vocative")


def _features(rule, fragment, verb):
    parts = fragment.split(".") if fragment else []
    features = {}
    for part in parts:
        name = "case" if part in CASES else "gender" if part in GENDERS else \
            "number" if part in ("singular", "plural") else "person"
        features[name] = part
    if verb:
        _, tense, voice, mood = _rule_identity(rule)
        features.update({"tense": tense, "voice": VOICE_FULL[voice], "mood": mood})
        if rule.startswith("eimi"):
            features.pop("voice")
    return features


def _parsing(features):
    return " ".join(filter(None, [features.get("tense"), features.get("voice"), features.get("mood"),
                                  ORDINAL.get(features.get("person"), ""), features.get("case"),
                                  features.get("gender"), features.get("number")]))


def build():
    import sys
    sys.path.insert(0, ".")
    from text_fabric.fabric_utils import load_n1904

    lines = _body_lines()
    corrected = []
    verb_charts, nominal_charts = _verb_charts(lines, corrected), _nominal_charts(lines)
    forms = _gnt_forms(load_n1904().api)
    liquid = _liquid_verbs(forms)
    lemma_counts, lemma_genders = collections.Counter(), collections.defaultdict(collections.Counter)
    for (form, lemma, cls, *_rest), count in forms.items():
        lemma_counts[lemma] += count
    for (form, lemma, cls, tense, voice, mood, person, case, gender, number, two), count in forms.items():
        if cls == "noun":
            lemma_genders[lemma][gender] += count
    dominant = {lemma: genders.most_common(1)[0][0] for lemma, genders in lemma_genders.items()}

    # rule -> pattern -> fragment -> charts printing it; the first chart's cell is the item's form
    printed = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
    patterns = collections.defaultdict(dict)
    for chart in verb_charts + nominal_charts:
        verb = "mood" in chart
        pattern = patterns[chart["rule"]].setdefault(chart["pattern"], {
            "name": VERB_PATTERN_NAMES.get(chart["pattern"], chart["pattern"]),
            "type": "verb" if verb else "noun", "charts": [], "source": [], "slots": []})
        if chart["lexical_form"] not in pattern["charts"]:
            pattern["charts"].append(chart["lexical_form"])
        if chart["source"] not in pattern["source"]:
            pattern["source"].append(chart["source"])
        if verb:
            pattern.update({"tense": chart["tense"], "aspect": ASPECTS.get(chart["tense"]),
                            "voice": VOICE_FULL[_rule_identity(chart["rule"])[2]], "mood": chart["mood"]})
        for slot, cell in chart["slots"].items():
            printed[chart["rule"]][chart["pattern"]][_fragment(slot, chart["gender"])].append((chart, cell))

    endings = {}
    for chart in verb_charts:
        identity = _rule_identity(chart["rule"])[1:3]
        endings[id(chart)] = _chart_endings(chart, [
            other for other in verb_charts if other is not chart and len(other["slots"]) > 1
            and (other["lemma"], other["stem_class"], _rule_identity(other["rule"])[1:3]) ==
            (chart["lemma"], chart["stem_class"], identity)])

    # every GNT form, filed under the rule, pattern and slot it fills
    found = collections.defaultdict(collections.Counter)      # (rule, pattern, fragment) -> (form, lemma)
    totals = collections.Counter()                             # (rule, fragment) -> occurrences
    irregular = collections.defaultdict(set)                   # rule -> suppletive lemmas
    for (form, lemma, cls, tense, voice, mood, person, case, gender, number, two), count in forms.items():
        if not mood:
            continue
        placed = _verb_slot(lemma, tense, voice, mood, person, case, gender, number, two)
        if not placed or placed[0] not in printed:
            continue
        rule, fragment = placed
        totals[(rule, fragment)] += count
        pattern, family = _verb_pattern(lemma, rule, two, liquid)
        charts = printed[rule].get(pattern, {}).get(fragment)
        if not charts:
            continue
        if family and family not in {_family(fold_greek(chart["lemma"])) for chart, _ in charts}:
            continue
        if pattern != "εἰμί" and not any(_ends_like(form, *endings[id(chart)][_slot_of(chart, fragment)])
                                          for chart, _ in charts):
            continue
        if fold_greek(lemma) not in WITHHELD:
            found[(rule, pattern, fragment)][(form, lemma)] += count
        if rule.split("-")[0] not in ("pres", "impf") and fold_greek(lemma).endswith(SUPPLETIVE):
            irregular[rule].add(lemma)

    nominal_tokens = collections.defaultdict(list)
    for (form, lemma, cls, tense, voice, mood, person, case, gender, number, two), count in forms.items():
        if case and not mood:
            nominal_tokens[lemma].append((form, (case, number), gender, count, cls))
    for chart in nominal_charts:
        chart["lexical_form"] = _lexical(chart["lexical_form"])
        chart["lemma_gender"] = dominant.get(chart["lexical_form"])
    groups = collections.defaultdict(list)
    for chart in nominal_charts:
        groups[chart["group"]].append(chart)
    # A word belongs to the one group it fits best: a chart printing few slots fits more words than
    # it describes.
    fits = collections.defaultdict(dict)
    for group, charts in groups.items():
        lead = charts[0]
        if not re.match(r"[na]-", lead["pattern"]):
            if lead["lexical_form"] in nominal_tokens:
                fits[lead["lexical_form"]][group] = (1,)
            continue
        pool = "noun" if lead["rule"].startswith("decl") else "adj"
        for lemma, tokens in nominal_tokens.items():
            if tokens[0][4] == pool:
                fit = _nominal_fit(charts, lemma, [token[:4] for token in tokens], dominant.get(lemma))
                if fit:
                    fits[lemma][group] = fit
    for lemma, scores in fits.items():
        for group in [_best_group(lemma, scores, groups)]:
            charts = groups[group]
            lead = charts[0]
            for form, slot, gender, count, _ in nominal_tokens[lemma]:
                chart_gender = _chart_gender(charts, gender)
                fragment = _fragment(slot, chart_gender)
                if chart_gender is False or fragment not in printed[lead["rule"]][lead["pattern"]]:
                    continue
                totals[(lead["rule"], fragment)] += count
                if fold_greek(lemma) not in WITHHELD:
                    found[(lead["rule"], lead["pattern"], fragment)][(form, lemma)] += count

    structure, items = {}, {}
    sequence = {rule: order for order, rule in enumerate(sorted({c["rule"] for c in verb_charts}), start=100)}
    for order, chart in enumerate(nominal_charts, start=1):
        sequence.setdefault(chart["rule"], order)
    for rule in sorted(printed, key=sequence.get):
        verb = rule in {chart["rule"] for chart in verb_charts}
        node = {"name": " ".join(filter(None, [TENSE_NAMES.get(_rule_identity(rule)[0]),
                                                "" if rule.startswith("eimi") else VOICE_NAMES[_rule_identity(rule)[2]],
                                                MOOD_NAMES[_rule_identity(rule)[3]],
                                                "of εἰμί" if rule.startswith("eimi") else ""]))
                if verb else RULE_NAMES.get(rule, rule),
                "sequence": sequence[rule], "pos_lex_category": "verb" if verb else "noun",
                "morph_rule_description": _describe(rule) if verb else "Case and number forms as the grammars print them.",
                "patterns": {}}
        for pattern_name, fragments in printed[rule].items():
            pattern = {**patterns[rule][pattern_name], "slots": []}
            word = not verb and not re.match(r"[na]-", pattern_name) or pattern_name == "εἰμί"
            for fragment, charts in fragments.items():
                candidates = found[(rule, pattern_name, fragment)]
                if totals[(rule, fragment)] < MIN_OCCURRENCES or sum(candidates.values()) < MIN_PATTERN_OCCURRENCES \
                        or all(lemma_counts[lemma] < KNOWN_FREQUENCY for _, lemma in candidates):
                    continue
                chart, cell = charts[0]
                key = "::".join(filter(None, [rule, pattern_name, fragment]))
                features = _features(rule, fragment, verb)
                items[key] = {"key": key, "parent": f"{rule}::{pattern_name}", "rule": rule,
                              "pattern": pattern_name, "form": cell, "lexical_form": chart["lexical_form"],
                              "parsing": _parsing(features), "features": features,
                              "gnt_occurrences": totals[(rule, fragment)],
                              "gnt_forms": _ranked(candidates, lemma_counts, irregular[rule], word)}
                pattern["slots"].append(key)
            if pattern["slots"]:
                node["patterns"][f"{rule}::{pattern_name}"] = pattern
        if node["patterns"]:
            structure[rule] = node
    return structure, items, corrected


def _slot_of(chart, fragment):
    """The chart's own slot for an item fragment."""
    return next(slot for slot in chart["slots"] if _fragment(slot, chart["gender"]) == fragment)


def write():
    structure, items, corrected = build()
    existing = json.loads(GRAMMAR_PATH.read_text(encoding="utf-8"))
    # Hand-written prose on a rule is kept. The derivation owns the forms; it does not own what
    # someone wrote about them.
    for rule, node in existing.get("structure", {}).items():
        if rule in structure:
            structure[rule].update({k: v for k, v in node.items()
                                    if k in ("teaching_note", "morph_recipe", "difficulty_tier")})
            if node.get("morph_rule_description") and node.get("teaching_note"):
                structure[rule]["morph_rule_description"] = node["morph_rule_description"]
    GRAMMAR_PATH.write_text(json.dumps(
        {"source": {"charts": "BBGG appendix: the Overview charts, the MBG-keyed verb and participle "
                              "charts, and the declension, adjective and pronoun charts; the article, "
                              "relative and personal pronouns from GrammarSummaries",
                    "patterns": "Each chart is filed under the pattern the appendix prints over it: MBG's "
                                "code for a noun or adjective, the verb chart's heading (thematic, "
                                "contracted, liquid, athematic, second aorist) for a verb. A pronoun, the "
                                "article and the irregular adjectives are each their own pattern.",
                    "items": f"A slot is an item where CenterBLC/N1904 uses it at least {MIN_OCCURRENCES} "
                             f"times across its rule and {MIN_PATTERN_OCCURRENCES} in its pattern, on a word occurring "
                             f"{KNOWN_FREQUENCY} times or more. form is the "
                             f"chart's; gnt_forms are up to {GNT_FORMS} of the GNT's own, one per known word, "
                             f"regular forms first, none of them a word verify.WITHHELD keeps off the cards.",
                    "corrected_forms": corrected},
         "structure": structure, "items": items},
        ensure_ascii=False, indent=1), encoding="utf-8")
    return len(structure), len(items)


if __name__ == "__main__":
    print("rules %d | items %d" % write())

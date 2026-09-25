"""Builds grammar_scaffolding.json from the paradigm charts the builder recovered.

**Why not Text-Fabric.** TF carries every attested form with full parsing, which makes it the
right source for lexical data and the wrong one for paradigms: only 18 verbs attest all six
present active indicative forms, exactly one attests all six imperfect active indicative, and
λύω - the paradigm verb every grammar uses precisely because it is regular - barely occurs in
the corpus at all. A teaching paradigm is not something the New Testament contains. It is
something a grammar prints, which is where these come from. TF is used afterwards, to check the
forms that *are* attested and flag the ones that disagree.

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
"""

import collections
import json
import re
import unicodedata
from pathlib import Path

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


def _fold(text):
    stripped = unicodedata.normalize("NFD", text or "")
    return unicodedata.normalize(
        "NFC", "".join(c for c in stripped if not unicodedata.combining(c))).lower()


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
    """A chart printing one middle/passive column fills both rules, as the Overviews do."""
    return [f"{tense}-mid-{mood}", f"{tense}-pas-{mood}"]


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


def _nominal(rule, genders=(None,)):
    return [(rule, gender) for gender in genders]


# The declension, adjective and pronoun grids from "First Declension Nouns" on. A column is
# (rule, gender); nouns carry no gender in their keys, and a masc & fem column carries none either.
# The article and relative pronoun printed beside the first declension come from GrammarSummaries.
APPENDIX_NOMINALS = [
    _nominal("decl1") * 4 + [None] * 3,
    _nominal("decl1") * 4 + [None] * 3,
    _nominal("decl2") * 6,
    _nominal("decl3") * 6,
    _nominal("decl3") * 6,
    _nominal("decl3") * 6,
    _nominal("decl3") * 6,
    _nominal("adjective-2-1-2", GENDERS) * 2,
    _nominal("pronoun-demonstrative", GENDERS) + _nominal("adjective-irregular", GENDERS),
    _nominal("adjective-irregular", GENDERS) + _nominal("pronoun-indefinite-relative", GENDERS),
    _nominal("adjective-3-1-3", GENDERS) * 2,
    _nominal("adjective-2-2", (None, "neuter")) + _nominal("adjective-3-3", (None, "neuter"))
    + _nominal("pronoun-personal", GENDERS),
    _nominal("adjective-3-3", (None, "neuter")) * 2,
    _nominal("pronoun-interrogative", (None, "neuter")) + _nominal("pronoun-indefinite", (None, "neuter"))
    + _nominal("numeral", GENDERS),
]

# Cells the appendix has wrong, by (rule, lemma, slot). Each is a dropped letter, a doubled
# ending, or a form printed in the wrong row; the corrected form is the one the parallel columns
# and the grammars' own rules give.
CORRECTIONS = {
    ("pres-mid-ind", "φανερόω", ("third_person", "plural")): "φανεροῦνται",
    ("pres-pas-ind", "φανερόω", ("third_person", "plural")): "φανεροῦνται",
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
            rule, gender = column
            slots = {ROW_SLOTS[label]: cells[index] for label, cells in grid.items()
                     if index < len(cells) and cells[index] != EMPTY}
            found.append({"resource": "BBGG", "section": "Appendix", "rule": rule, "gender": gender,
                          "lexical_form": next(iter(slots.values())), "page": None, "slots": slots})
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


BREATHING = ("\u0313", "\u0314")


def _misplaced_breathing(form):
    """Whether a form carries a breathing mark somewhere Greek cannot put one.

    A breathing sits on the first vowel of a word and nowhere else, so one appearing later is
    export damage rather than an unusual spelling. This separates the two kinds of entry in the
    unverified list: a form the corpus simply never happens to use, and a form that is wrong.
    Flagged, never corrected - the paradigm is reproduced as the book prints it."""
    text = unicodedata.normalize("NFD", re.sub(r"\(.*?\)", "", form or ""))
    seen = False
    for index, character in enumerate(text):
        if unicodedata.combining(character) == 0 and character.isalpha():
            if seen and index > 2 and any(mark in text[index:] for mark in BREATHING):
                return True
            seen = True
    return False


def _attested(api):
    """Every surface form in the corpus, accent-folded, for checking chart forms against."""
    index = collections.defaultdict(set)
    for node in api.F.otype.s("word"):
        text = (api.F.text.v(node) or "").strip()
        if text:
            index[_fold(text)].add(
                (api.F.tense.v(node), api.F.voice.v(node), api.F.mood.v(node)))
    return index


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
# Rules an earlier derivation produced that this one replaces: charts filed under a page heading
# rather than what they are, and participles held under one rule with no tense or voice.
RETIRED_RULES = {"noun-rules", "participle-forms", "adjective-decl3", "noun-irregular", "decl1-decl2",
                 "case-endings"}
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

# Charts that print one gender per column give a separate paradigm per gender, so the gender is
# carried by the lexeme rather than by a column header. Naming it in the key matters: student
# progress already records the article as "article::ὁ::nominative.masculine.singular", and a key
# without the gender would never match what a student has actually learned.
GENDER_BY_LEXEME = {
    "ὁ": "masculine", "ἡ": "feminine", "τό": "neuter",
    "ὅς": "masculine", "ἥ": "feminine", "ὅ": "neuter",
    "αὐτός": "masculine", "αὐτή": "feminine", "αὐτό": "neuter",
    "οὗτος": "masculine", "αὕτη": "feminine", "τοῦτο": "neuter",
    "ἐκεῖνος": "masculine", "ἐκείνη": "feminine", "ἐκεῖνο": "neuter",
}
TENSE_NAMES = {"pres": "Present", "impf": "Imperfect", "fut": "Future", "perf": "Perfect",
               "aor1": "First Aorist", "aor2": "Second Aorist"}
MOOD_NAMES = {"indicative": "Indicative", "subjunctive": "Subjunctive",
              "imperative": "Imperative", "infinitive": "Infinitive", "participle": "Participle"}


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40]


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


def _describe(rule, spec):
    voice = VOICE_NAMES[spec["voice"]]
    tense = TENSE_NAMES.get(rule.split("-")[0], spec["tense"].title())
    mood = MOOD_NAMES[spec["mood"]]
    if rule.startswith("eimi"):
        return (f"{tense} {mood.lower()} of εἰμί. The verb is athematic and irregular, so its "
                f"forms are learned as a set rather than built from a rule.")
    return (f"{tense} {voice.lower()} {mood.lower()}, as BBGG's appendix prints it on the "
            f"paradigm verb and, where it prints them, on contract, liquid and athematic verbs. "
            f"The forms are given whole rather than derived, which is how the charts state them.")


# Frequencies come from the vocabulary file rather than a second corpus pass. A verb paradigm's
# lexical_form is an inflected form (elyon is not a lemma), so most verb paradigms get none.
LEMMA_FREQUENCY = {}


def _load_frequencies():
    path = Path("data/curriculum_data/vocabulary_scaffolding.json")
    if not path.exists():
        return {}
    items = json.loads(path.read_text(encoding="utf-8")).get("items", {})
    return {lemma: entry.get("frequency") for lemma, entry in items.items()
            if entry.get("frequency")}


def build(verify=True):
    global LEMMA_FREQUENCY
    LEMMA_FREQUENCY = _load_frequencies()
    lines = _body_lines()
    corrected = []
    # The Overviews come first, so where the appendix repeats λύω the Overview's paradigm stands.
    verb_paradigms = []
    for rule, spec in sorted(_verb_rules(lines).items()):
        tense_key = _rule_identity(rule)[0]
        lemma = "εἰμί" if rule.startswith("eimi") else OVERVIEW_LEMMAS.get((tense_key, spec["voice"]), "λύω")
        stem = "irregular" if lemma == "εἰμί" else "second aorist" if tense_key == "aor2" else "thematic"
        verb_paradigms.append({**spec, "rule": rule, "lemma": lemma, "stem_class": stem, "gender": None})
    verb_paradigms += _appendix_verbs(lines, corrected)
    case_charts = _appendix_nominals(lines) + _case_paradigms()

    attested = {}
    if verify:
        import sys
        sys.path.insert(0, ".")
        from text_fabric.fabric_utils import load_n1904
        attested = _attested(load_n1904().api)

    structure, items, unverified = {}, {}, []

    def add(rule, rule_meta, paradigm_key, lexical_form, slots, slot_features, source, extra=None):
        node = structure.setdefault(rule, {**rule_meta, "paradigms": {}})
        if paradigm_key in node["paradigms"]:
            return
        slot_keys = []
        for slot, form in slots.items():
            features = slot_features(slot)
            fragment = ".".join(str(features[name]) for name in features if name in
                                ("person", "case", "gender", "number"))
            key = f"{paradigm_key}::{fragment}" if fragment else paradigm_key
            parsing = " ".join(
                [rule_meta.get("_parsing_prefix", "")] +
                [ORDINAL.get(features.get("person"), ""), features.get("case", ""),
                 features.get("gender", ""), features.get("number", "")]).split()
            items[key] = {
                "key": key, "parent": paradigm_key, "rule": rule, "form": form,
                "parsing": " ".join(parsing), "features": features,
                "lexical_form": lexical_form,
            }
            slot_keys.append(key)
            if verify and form:
                bare = _fold(re.sub(r"\(.*?\)", "", form).split(",")[0].strip())
                if bare and bare not in attested:
                    unverified.append(key)
        paradigm = {"type": rule_meta["pos_lex_category"], "lexical_form": lexical_form,
                    "source": source, "slots": slot_keys}
        paradigm.update({k: v for k, v in (rule_meta.get("_paradigm_features") or {}).items()})
        paradigm.update({k: v for k, v in (extra or {}).items() if v})
        frequency = LEMMA_FREQUENCY.get(extra.get("lemma") if extra else None) or LEMMA_FREQUENCY.get(lexical_form)
        if frequency:
            paradigm["gnt_lemma_frequency"] = frequency
        node["paradigms"][paradigm_key] = paradigm

    sequence = {rule: order for order, rule in
                enumerate(sorted({p["rule"] for p in verb_paradigms}), start=100)}
    for spec in verb_paradigms:
        rule, eimi = spec["rule"], spec["rule"].startswith("eimi")
        meta = {
            "name": " ".join(filter(None, [
                TENSE_NAMES.get(_rule_identity(rule)[0], spec["tense"].title()),
                "" if eimi else VOICE_NAMES[spec["voice"]],
                MOOD_NAMES[spec["mood"]], "of εἰμί" if eimi else ""])),
            "sequence": sequence[rule], "pos_lex_category": "verb",
            "morph_rule_description": _describe(rule, spec),
            "_paradigm_features": {"tense": spec["tense"], "aspect": ASPECTS.get(spec["tense"]),
                                   "voice": VOICE_FULL[spec["voice"]], "mood": spec["mood"]},
            "_parsing_prefix": " ".join(filter(None, [
                spec["tense"], "" if eimi else VOICE_FULL[spec["voice"]], spec["mood"]])),
        }

        def features_for(slot, spec=spec):
            identity = {"tense": spec["tense"], "voice": VOICE_FULL[spec["voice"]], "mood": spec["mood"]}
            if not isinstance(slot, tuple):
                return identity
            if spec["mood"] == "participle":
                gender = {"gender": spec["gender"]} if spec["gender"] else {}
                return {"case": slot[0], **gender, "number": slot[1], **identity}
            return {"person": slot[0], "number": slot[1], **identity}

        add(rule, meta, f"{rule}::{spec['lexical_form']}", spec["lexical_form"], spec["slots"],
            features_for, [{"resource": "BBGG", "chapter": "Appendix", "header": spec["chart"], "page": None}],
            {"lemma": spec["lemma"], "stem_class": spec["stem_class"], "gender": spec["gender"]})

    for order, chart in enumerate(case_charts, start=1):
        rule = chart.get("rule") or LEXEME_RULES.get(
            chart["lexical_form"], CASE_RULES.get(chart["section"], _slug(chart["section"])))
        meta = {"name": RULE_NAMES.get(rule, chart["section"]), "sequence": order,
                "pos_lex_category": "noun",
                "morph_rule_description": f"Case and number forms as {chart['resource']} prints them.",
                "_parsing_prefix": ""}
        gender = chart.get("gender") or GENDER_BY_LEXEME.get(chart["lexical_form"])
        add(rule, meta, f"{rule}::{chart['lexical_form']}", chart["lexical_form"], chart["slots"],
            lambda slot, gender=gender: (
                {"case": slot[0], "gender": gender, "number": slot[1]} if gender
                else {"case": slot[0], "number": slot[1]}),
            [{"resource": chart["resource"], "chapter": "Appendix", "header": chart["section"],
              "page": chart["page"]}])

    for node in structure.values():
        node.pop("_parsing_prefix", None)
        node.pop("_paradigm_features", None)
    return structure, items, unverified, corrected


def write(verify=True):
    structure, items, unverified, corrected = build(verify=verify)
    existing = json.loads(GRAMMAR_PATH.read_text(encoding="utf-8"))
    # Hand-written prose on a rule - teaching_note, morph_recipe, drill_lexemes - is kept.
    # The derivation owns the forms; it does not own what someone wrote about them.
    for rule, node in existing.get("structure", {}).items():
        if rule in RETIRED_RULES:
            continue
        if rule in structure:
            keep = {k: v for k, v in node.items()
                    if k in ("teaching_note", "morph_recipe", "drill_lexemes",
                             "difficulty_tier", "morph_rule_description")}
            structure[rule] = {**structure[rule], **keep}
        else:
            structure[rule] = node
    for key, item in existing.get("items", {}).items():
        if item.get("rule") in RETIRED_RULES:
            continue
        if item.get("rule") in structure and key not in items:
            continue    # a rule this run regenerated: an old key it no longer emits is stale
        items[key] = {**item, **items.get(key, {})}

    GRAMMAR_PATH.write_text(json.dumps(
        {"source": {"paradigms": "BBGG appendix: the Overview charts, the MBG-keyed verb and "
                                 "participle charts, and the declension, adjective and pronoun "
                                 "charts; the article, relative and personal pronouns from "
                                 "GrammarSummaries",
                    "corrected_forms": corrected,
                    "verification": "Forms are checked against CenterBLC/N1904; a form the "
                                    "corpus does not attest is listed in unverified_forms "
                                    "rather than dropped, since a teaching paradigm is not "
                                    "expected to occur whole in the New Testament.",
                    "unverified_forms": sorted(unverified),
                    "likely_damaged": sorted(
                        key for key in unverified if _misplaced_breathing(items[key]["form"]))},
         "structure": structure, "items": items},
        ensure_ascii=False, indent=1), encoding="utf-8")
    return len(structure), len(items), len(unverified)


if __name__ == "__main__":
    print("rules %d | items %d | unattested forms %d" % write())

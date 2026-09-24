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
MOODS = {"indicative": "ind", "subjunctive": "subj", "imperative": "impv", "infinitive": "inf"}
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


def _case_paradigms():
    """Declensions, the article, pronouns and adjectives, from the builder's typed output.

    These already carry CASE_NUMBER_SLOTS, so unlike the verb charts they need no
    reinterpretation - only a rule name and a filter for the ones printing bare endings."""
    found = []
    for resource in ("GrammarSummaries", "KAIROS", "BBGG"):
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


# Chart section names mapped onto rule names. Book knowledge, so it is data - and it is a dozen
# strings rather than a rule engine. Anything unlisted is slugified from its section.
CASE_RULES = {
    "Definite Article": "article",
    "First and Second Declension Nouns": "decl1-decl2",
    "Third Declension": "decl3",
    "Case Endings and Rules": "case-endings",
    "Personal Pronouns": "pronoun-personal",
    "§6 Pure Third Declension Adjectives": "adjective-decl3",
    "§8 Slightly Irregular": "noun-irregular",
    "§15 Participles": "participle-forms",
    "Participle": "participle-forms",
    "The Eight Noun Rules": "noun-rules",
    "Master Case Ending Chart": "case-endings",
}
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
              "imperative": "Imperative", "infinitive": "Infinitive"}


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
            f"paradigm verb. The forms are given whole rather than derived, which is how the "
            f"chart states them.")


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
    verb_rules = _verb_rules(lines)
    case_charts = _case_paradigms()

    attested = {}
    if verify:
        import sys
        sys.path.insert(0, ".")
        from text_fabric.fabric_utils import load_n1904
        attested = _attested(load_n1904().api)

    structure, items, unverified = {}, {}, []

    def add(rule, rule_meta, paradigm_key, lexical_form, slots, slot_features, source):
        node = structure.setdefault(rule, {**rule_meta, "paradigms": {}})
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
        frequency = LEMMA_FREQUENCY.get(lexical_form)
        if frequency:
            paradigm["gnt_lemma_frequency"] = frequency
        node["paradigms"][paradigm_key] = paradigm

    for order, (rule, spec) in enumerate(sorted(verb_rules.items()), start=100):
        base = {"case": None}
        meta = {
            "name": " ".join(filter(None, [
                TENSE_NAMES.get(rule.split("-")[0], spec["tense"].title()),
                VOICE_NAMES[spec["voice"]] if not rule.startswith("eimi") else "",
                MOOD_NAMES[spec["mood"]], "of εἰμί" if rule.startswith("eimi") else ""])),
            "sequence": order, "pos_lex_category": "verb",
            "morph_rule_description": _describe(rule, spec),
            "_paradigm_features": {"tense": spec["tense"], "aspect": ASPECTS.get(spec["tense"]),
                                   "voice": VOICE_FULL[spec["voice"]], "mood": spec["mood"]},
            "_parsing_prefix": " ".join(filter(None, [
                spec["tense"],
                "" if rule.startswith("eimi") else VOICE_FULL[spec["voice"]],
                spec["mood"]])),
        }
        paradigm_key = f"{rule}::{spec['lexical_form']}"

        def features_for(slot, spec=spec):
            if slot == "_" or not isinstance(slot, tuple):
                return {"tense": spec["tense"], "voice": VOICE_FULL[spec["voice"]],
                    "mood": spec["mood"]}
            person, number = slot
            return {"person": person, "number": number, "tense": spec["tense"],
                    "voice": VOICE_FULL[spec["voice"]], "mood": spec["mood"]}

        add(rule, meta, paradigm_key, spec["lexical_form"], spec["slots"], features_for,
            [{"resource": "BBGG", "chapter": "Appendix", "header": spec["chart"], "page": None}])

    for order, chart in enumerate(case_charts, start=1):
        rule = LEXEME_RULES.get(chart["lexical_form"],
                                CASE_RULES.get(chart["section"], _slug(chart["section"])))
        meta = {"name": chart["section"], "sequence": order, "pos_lex_category": "noun",
                "morph_rule_description":
                    f"Case and number forms as {chart['resource']} prints them under "
                    f"\"{chart['section']}\".",
                "_parsing_prefix": ""}
        paradigm_key = f"{rule}::{chart['lexical_form']}"
        gender = GENDER_BY_LEXEME.get(chart["lexical_form"])
        add(rule, meta, paradigm_key, chart["lexical_form"], chart["slots"],
            lambda slot, gender=gender: (
                {"case": slot[0], "gender": gender, "number": slot[1]} if gender
                else {"case": slot[0], "number": slot[1]}),
            [{"resource": chart["resource"], "chapter": "Appendix",
              "header": chart["section"], "page": chart["page"]}])

    for node in structure.values():
        node.pop("_parsing_prefix", None)
        node.pop("_paradigm_features", None)
    return structure, items, unverified


def write(verify=True):
    structure, items, unverified = build(verify=verify)
    existing = json.loads(GRAMMAR_PATH.read_text(encoding="utf-8"))
    # Hand-written prose on a rule - teaching_note, morph_recipe, drill_lexemes - is kept.
    # The derivation owns the forms; it does not own what someone wrote about them.
    for rule, node in existing.get("structure", {}).items():
        if rule in structure:
            keep = {k: v for k, v in node.items()
                    if k in ("teaching_note", "morph_recipe", "drill_lexemes",
                             "difficulty_tier", "morph_rule_description")}
            structure[rule] = {**structure[rule], **keep}
        else:
            structure[rule] = node
    for key, item in existing.get("items", {}).items():
        if item.get("rule") in structure and key not in items:
            continue    # a rule this run regenerated: an old key it no longer emits is stale
        items[key] = {**item, **items.get(key, {})}

    GRAMMAR_PATH.write_text(json.dumps(
        {"source": {"paradigms": "BBGG appendix Overview charts; declension and pronoun charts "
                                 "from GrammarSummaries and KAIROS",
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

"""Fills the traversal's empty usages with the keys that gate them.

A usage becomes available to a student only when `check_traversal_specific_uses` finds both
halves: the syntactic category (has the student met adverbial cause?) and at least one of the
grammatical forms it is built from (can the student form an aorist participle?). Until both are
present the usage is dark, which is why every `{}` in the traversal made the randomizer raise.

`syntactic_item` points into syntax_scaffolding, `grammatical_items` into grammar_scaffolding.
Both are checked here rather than trusted - a key that does not resolve is a silent dead branch.

`grammatical_items` lists the forms that would actually appear in the construction, not every
form of the paradigm. An adverbial participle agrees with the subject and so shows up in the
nominative; a hina clause needs a third-person subjunctive. The check is `any`, so the list
means "the student can build this if they know any one of these".
"""

import json
import re
from pathlib import Path

TRAVERSAL_PATH = Path("tasks/card_randomization/card_randomize_traversal.py")
GRAMMAR = json.loads(
    Path("data/curriculum_data/grammar_scaffolding.json").read_text(encoding="utf-8"))
SYNTAX = json.loads(
    Path("data/curriculum_data/syntax_scaffolding.json").read_text(encoding="utf-8"))

ADVERBIAL = "participle/verbal-participles/dependent-verbal-participles/adverbial-circumstantial"
OTI = "moods/indicative/indicative-ὃτι"
HINA = "moods/subjunctive/dependent-subordinate-clauses/ἳνα-subjunctive"


def _items(prefix, suffix=""):
    """Every grammar item under a rule, optionally narrowed to one slot."""
    return sorted(k for k in GRAMMAR["items"]
                  if k.startswith(prefix) and k.endswith(suffix))


def _participles(*slots):
    """Participle forms in the given slots, across every paradigm the charts supply."""
    found = []
    for slot in slots:
        found += _items("participle-forms::", f"::{slot}")
    return sorted(found)


def _finite(rules, slot="third_person.singular"):
    return sorted(k for rule in rules for k in _items(f"{rule}::", f"::{slot}"))


INDICATIVE = ["pres-act-ind", "impf-act-ind", "aor1-act-ind", "aor2-act-ind", "perf-act-ind"]
SUBJUNCTIVE = ["pres-act-subj", "aor1-act-subj", "aor2-act-subj"]
INFINITIVES = ["pres-act-inf", "aor1-act-inf", "aor2-act-inf", "perf-act-inf"]
NOMINALS = ["decl1", "decl2", "decl3"]

# usage path -> (syntactic_item, grammatical_items)
WIRING = {
    # --- adverbial dependent clauses -----------------------------------------------------
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.causal.infinitive": (f"infinitive/adverbial/cause", _items("aor1-act-inf::")
                                    + _items("pres-act-inf::")),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.causal.adverbial_participle": (f"{ADVERBIAL}/cause", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.causal.oti_indicative": (f"{OTI}/causal-adverbial", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.concessive.adverbial_participle": (f"{ADVERBIAL}/concession", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.concessive.ei_kai_indicative": ("conjunctions/adverbial-functions/causal", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.conditional.first_class": ("moods/indicative/conditional-indicative", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.conditional.second_class": ("moods/indicative/conditional-indicative", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.conditional.third_class": (
        "moods/subjunctive/dependent-subordinate-clauses/subjunctive-conditional-sentences",
        _finite(SUBJUNCTIVE)),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.manner_means.articular_infinitive": ("infinitive/adverbial/means", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.manner_means.adverbial_participle": (f"{ADVERBIAL}/means", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.manner_means.relative_pn_hon": ("pronouns/semantic-categories/relative-pronouns",
                                               _items("pronoun-relative::")),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.purpose.infinitive": ("infinitive/adverbial/purpose", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.purpose.adverbial_participle": (f"{ADVERBIAL}/purpose-telic", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.purpose.hina_subjunctive": (f"{HINA}/purpose-ἳνα-clause-k-final-telic-ἳνα",
                                           _finite(SUBJUNCTIVE)),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.purpose.relative_pn_hoitines": ("pronouns/semantic-categories/relative-pronouns",
                                               _items("pronoun-relative::")),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.resultative.infinitive": ("infinitive/adverbial/result", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.resultative.adverbial_participle": (f"{ADVERBIAL}/result", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.resultative.hina_subjunctive": (
        f"{HINA}/result-ἳνα-clause-k-consecutive-ecbatic-ἳνα", _finite(SUBJUNCTIVE)),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.resultative.relative_adverb_hothen": (
        "conjunctions/adverbial-functions/result", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.time.articular_infinitive": ("infinitive/adverbial/time", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.time.adverbial_participle": (f"{ADVERBIAL}/temporal", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.time.hote_indicative": ("conjunctions/adverbial-functions/temporal", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.time.relative_pn": ("pronouns/semantic-categories/relative-pronouns",
                                   _items("pronoun-relative::")),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.comparative.adverbial_participle": (f"{ADVERBIAL}/manner", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.comparative.kathos_hos_indicative": (
        "conjunctions/adverbial-functions/comparative-manner", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.local.hopou_indicative": ("conjunctions/adverbial-functions/local-sphere", None),
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.local.relative_adverb_hou": ("conjunctions/adverbial-functions/local-sphere",
                                            _items("pronoun-relative::")),
    # --- relative sentence ------------------------------------------------------------------
    "sentence_construction_possibilitites.main_and_relative_sentence.substantival.indicative.subject": (f"{OTI}/substantival-ὃτι-clauses/subject-clause",
                                                 _items("pronoun-relative::")),
    "sentence_construction_possibilitites.main_and_relative_sentence.substantival.indicative.object": (
        f"{OTI}/substantival-ὃτι-clauses/direct-object-clause", _items("pronoun-relative::")),
    "sentence_construction_possibilitites.main_and_relative_sentence.substantival.indicative.independent": (
        "clauses-general/independent-clauses", _items("pronoun-relative::")),
    "sentence_construction_possibilitites.main_and_relative_sentence.substantival.subjunctive": (
        "moods/subjunctive/dependent-subordinate-clauses/subjunctive-indefinite-relative-clause",
        _items("pronoun-relative::")),
    "sentence_construction_possibilitites.main_and_relative_sentence.adjectival": ("pronouns/semantic-categories/relative-pronouns",
                            _items("pronoun-relative::")),
    # --- sentence vitals ---------------------------------------------------------------------
    "sentence_vitals.verb.finite_verb": ("voice/active/simple-active", _finite(INDICATIVE)),
    "sentence_vitals.verb.finite_with_infinitive_complement": ("infinitive/adverbial/complementary-supplementary",
                                                      None),
    "sentence_vitals.subject.nominative": ("nominative/primary-uses/subject",
                                  _finite(NOMINALS, "nominative.singular")),
    "sentence_vitals.subject.substantival_participle": ("participle/substantival-independent",
                                               _participles("nominative.singular")),
    "sentence_vitals.subject.hoti_indicative": (f"{OTI}/substantival-ὃτι-clauses/subject-clause", None),
    "sentence_vitals.subject.hina_subjunctive": (
        f"{HINA}/substantival-ἳνα-clause-k-sub-final-clause/subject-clause", _finite(SUBJUNCTIVE)),
    "sentence_vitals.subject.relative_pn_ho": ("pronouns/semantic-categories/relative-pronouns",
                                      _items("pronoun-relative::")),
    "sentence_vitals.object.accusative": ("accusative/substantival-uses-accusative/accusative-direct-object",
                                 _finite(NOMINALS, "accusative.singular")),
    "sentence_vitals.object.substantival_participle": ("participle/substantival-independent",
                                              _participles("accusative.singular")),
    "sentence_vitals.object.relative_clause": ("pronouns/semantic-categories/relative-pronouns",
                                      _items("pronoun-relative::")),
    "sentence_vitals.object.substantival_infinitive": ("infinitive/substantival/direct-object", None),
    "sentence_vitals.object.hoti_indicative": (f"{OTI}/substantival-ὃτι-clauses/direct-object-clause", None),
    "sentence_vitals.object.hina_subjunctive": (
        f"{HINA}/substantival-ἳνα-clause-k-sub-final-clause/direct-object-clause-k-content-ἳνα-clause",
        _finite(SUBJUNCTIVE)),
    # --- supplementary pieces -----------------------------------------------------------------
    "other_supplementary_pieces.extra_case_usage.genitive": ("genitive/adjectival/possessive-genitive",
                                       _finite(NOMINALS, "genitive.singular")),
    "other_supplementary_pieces.extra_case_usage.dative": ("dative/instrumental-dative-uses/dative-means-instrument",
                                     _finite(NOMINALS, "dative.singular")),
    "other_supplementary_pieces.adverbial.verbal_modification_proper": ("conjunctions/adverbial-functions", None),
    "other_supplementary_pieces.adverbial.substantival_modification": (
        "article/regular-uses-article/as-substantiver-certain-parts-speech", _items("article::")),
    "other_supplementary_pieces.prepositions": ("prepositions", None),
    "other_supplementary_pieces.particles": ("conjunctions/logical-functions", None),
}

# Fallbacks by construction, used wherever WIRING passes None for the grammatical side.
DEFAULT_ITEMS = {
    "adverbial_participle": lambda: _participles("nominative.singular"),
    "infinitive": lambda: sorted(k for rule in INFINITIVES for k in _items(f"{rule}::")),
    "articular_infinitive": lambda: sorted(k for rule in INFINITIVES for k in _items(f"{rule}::")),
    "oti_indicative": lambda: _finite(INDICATIVE),
    "ei_kai_indicative": lambda: _finite(INDICATIVE),
    "hote_indicative": lambda: _finite(INDICATIVE),
    "kathos_hos_indicative": lambda: _finite(INDICATIVE),
    "hopou_indicative": lambda: _finite(INDICATIVE),
    "first_class": lambda: _finite(INDICATIVE),
    "second_class": lambda: _finite(INDICATIVE),
    "substantival_infinitive": lambda: sorted(
        k for rule in INFINITIVES for k in _items(f"{rule}::")),
    "finite_with_infinitive_complement": lambda: sorted(
        k for rule in INFINITIVES for k in _items(f"{rule}::")),
    "hoti_indicative": lambda: _finite(INDICATIVE),
    "verbal_modification_proper": lambda: _finite(INDICATIVE),
    "relative_adverb_hothen": lambda: _items("pronoun-relative::"),
    "prepositions": lambda: _finite(NOMINALS, "dative.singular")
                            + _finite(NOMINALS, "accusative.singular"),
    "particles": lambda: _finite(INDICATIVE),
}


def resolve():
    """Every usage path with its two keys, and a report of anything that does not resolve."""
    wired, missing = {}, []
    for path, (syntactic, grammatical) in WIRING.items():
        leaf = path.rsplit(".", 1)[-1]
        if grammatical is None:
            grammatical = DEFAULT_ITEMS.get(leaf, list)()
        if syntactic not in SYNTAX["items"] and syntactic not in SYNTAX["structure"]:
            missing.append(("syntax", path, syntactic))
        unknown = [k for k in grammatical if k not in GRAMMAR["items"]]
        if unknown:
            missing.append(("grammar", path, unknown[:3]))
        if not grammatical:
            missing.append(("empty", path, "no grammatical items"))
        wired[path] = {"syntactic_item": syntactic, "grammatical_items": grammatical}
    return wired, missing


WIRING_PATH = Path("data/curriculum_data/traversal_wiring.json")


def write():
    wired, missing = resolve()
    if missing:
        raise ValueError(f"{len(missing)} usages do not resolve: {missing[:3]}")
    WIRING_PATH.write_text(json.dumps(wired, ensure_ascii=False, indent=1), encoding="utf-8")
    return len(wired)


if __name__ == "__main__":
    wired, missing = resolve()
    if not missing:
        write()
    print(f"usages wired: {len(wired)}")
    print(f"unresolved:   {len(missing)}")
    for kind, path, detail in missing:
        print(f"  [{kind}] {path} -> {detail}")

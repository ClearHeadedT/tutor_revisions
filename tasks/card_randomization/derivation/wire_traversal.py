"""Fills the traversal's empty usages with the keys that gate them.

    python -m tasks.card_randomization.derivation.wire_traversal

A usage becomes available to a student only when both halves are present: the syntactic category
(has the student met adverbial cause?) and the grammar the construction is built from (can they
form a participle?). `syntactic_item` points into syntax_scaffolding. `grammar_requires` is a list
of requirements, each a list of grammar groups (see data/curriculum_data/grammar_groups.py); the
student needs at least one group from every requirement. An articular infinitive needs an
infinitive and the article, so it carries two. `describe` is the syntax item whose definition the
model is shown, where that is not the gate itself; None shows none.

Grammar is gated by group, not by slot. A plan asks whether a construction can be built at all, and
leaves the forms to the model, which is handed the chart for the group it is to use.

Both halves are checked here rather than trusted - a key that does not resolve is a silent dead
branch. Usages left out of WIRING stay empty and are never offered:
  comparative.adverbial_participle     unattested; formation_instructions says nothing backs it
  substantival.indicative.independent  its formation describes an ordinary relative clause with an
                                       antecedent, which is adjectival
"""

import json
from pathlib import Path

from data.curriculum_data.grammar_groups import all_groups, groups_matching

SYNTAX = json.loads(
    Path("data/curriculum_data/syntax_scaffolding.json").read_text(encoding="utf-8"))

ADVERBIAL = "participle/verbal-participles/dependent-verbal-participles/adverbial-circumstantial"
OTI = "moods/indicative/indicative-ὃτι"
HINA = "moods/subjunctive/dependent-subordinate-clauses/ἳνα-subjunctive"
CONDITIONS = "conditional-sentences/ii-conditional-sentences-greek-especially-nt"
RELATIVE_SYNTAX = "pronouns/semantic-categories/relative-pronouns"

INDICATIVE = groups_matching(lambda g: g.endswith("-ind"))
SECONDARY_INDICATIVE = groups_matching(lambda g: g.endswith("-ind") and ("impf" in g or g.startswith("aor")))
SUBJUNCTIVE = groups_matching(lambda g: g.endswith("-subj"))
INFINITIVE = groups_matching(lambda g: g.endswith("-inf"))
PARTICIPLE = groups_matching(lambda g: g.endswith("-ptc"))
ARTICLE = ["article"]
RELATIVE = ["pronoun-relative"]

DEPENDENT = "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial"
RELATIVE_SENTENCE = "sentence_construction_possibilitites.main_and_relative_sentence"

# usage path -> (syntactic_item, grammar_requires[, describe])
WIRING = {
    f"{DEPENDENT}.causal.infinitive": ("infinitive/adverbial/cause", [INFINITIVE, ARTICLE]),
    f"{DEPENDENT}.causal.adverbial_participle": (f"{ADVERBIAL}/cause", [PARTICIPLE]),
    f"{DEPENDENT}.causal.oti_indicative": (f"{OTI}/causal-adverbial", [INDICATIVE]),
    f"{DEPENDENT}.concessive.adverbial_participle": (f"{ADVERBIAL}/concession", [PARTICIPLE]),
    # The syntax scaffolding has no concessive conjunction. εἰ καί is gated on the concessive
    # category, which the student must know, and no definition is shown: that item describes a
    # participle, and the formation notes already define the clause.
    f"{DEPENDENT}.concessive.ei_kai_indicative": (f"{ADVERBIAL}/concession", [INDICATIVE], None),
    f"{DEPENDENT}.conditional.first_class": (f"{CONDITIONS}/first-class-condition", [INDICATIVE]),
    f"{DEPENDENT}.conditional.second_class": (f"{CONDITIONS}/second-class-condition", [SECONDARY_INDICATIVE]),
    f"{DEPENDENT}.conditional.third_class": (f"{CONDITIONS}/third-class-condition", [SUBJUNCTIVE]),
    f"{DEPENDENT}.manner_means.articular_infinitive": ("infinitive/adverbial/means", [INFINITIVE, ARTICLE]),
    f"{DEPENDENT}.manner_means.adverbial_participle": (f"{ADVERBIAL}/means", [PARTICIPLE]),
    f"{DEPENDENT}.manner_means.relative_pn_hon": (RELATIVE_SYNTAX, [RELATIVE, INDICATIVE]),
    f"{DEPENDENT}.purpose.infinitive": ("infinitive/adverbial/purpose", [INFINITIVE]),
    f"{DEPENDENT}.purpose.adverbial_participle": (f"{ADVERBIAL}/purpose-telic", [PARTICIPLE]),
    f"{DEPENDENT}.purpose.hina_subjunctive": (f"{HINA}/purpose-ἳνα-clause-k-final-telic-ἳνα", [SUBJUNCTIVE]),
    # ὅστις has no chart of its own; ὅς is the nearest the student can have met.
    f"{DEPENDENT}.purpose.relative_pn_hoitines": (f"{RELATIVE_SYNTAX}/ὅστις-called-indefinite-better",
                                                  [RELATIVE, INDICATIVE]),
    f"{DEPENDENT}.resultative.infinitive": ("infinitive/adverbial/result", [INFINITIVE]),
    f"{DEPENDENT}.resultative.adverbial_participle": (f"{ADVERBIAL}/result", [PARTICIPLE]),
    f"{DEPENDENT}.resultative.hina_subjunctive": (f"{HINA}/result-ἳνα-clause-k-consecutive-ecbatic-ἳνα",
                                                  [SUBJUNCTIVE]),
    # ὅθεν and οὗ are adverbs: the clause needs a finite verb, not a declined pronoun.
    f"{DEPENDENT}.resultative.relative_adverb_hothen": ("conjunctions/adverbial-functions/result", [INDICATIVE]),
    f"{DEPENDENT}.time.articular_infinitive": ("infinitive/adverbial/time", [INFINITIVE, ARTICLE]),
    f"{DEPENDENT}.time.adverbial_participle": (f"{ADVERBIAL}/temporal", [PARTICIPLE]),
    f"{DEPENDENT}.time.hote_indicative": ("conjunctions/adverbial-functions/temporal", [INDICATIVE]),
    f"{DEPENDENT}.time.relative_pn": (RELATIVE_SYNTAX, [RELATIVE, INDICATIVE]),
    f"{DEPENDENT}.comparative.kathos_hos_indicative": ("conjunctions/adverbial-functions/comparative-manner",
                                                      [INDICATIVE]),
    f"{DEPENDENT}.local.hopou_indicative": ("conjunctions/adverbial-functions/local-sphere", [INDICATIVE]),
    f"{DEPENDENT}.local.relative_adverb_hou": ("conjunctions/adverbial-functions/local-sphere", [INDICATIVE]),

    # A headless relative clause standing in the subject or object slot.
    f"{RELATIVE_SENTENCE}.substantival.indicative.subject": (
        f"{RELATIVE_SYNTAX}/ὅς/unusual-uses/antecedent-complexities/omission-antecedent", [RELATIVE, INDICATIVE]),
    f"{RELATIVE_SENTENCE}.substantival.indicative.object": (
        f"{RELATIVE_SYNTAX}/ὅς/unusual-uses/antecedent-complexities/omission-antecedent", [RELATIVE, INDICATIVE]),
    f"{RELATIVE_SENTENCE}.substantival.subjunctive": (
        "moods/subjunctive/dependent-subordinate-clauses/subjunctive-indefinite-relative-clause",
        [RELATIVE, SUBJUNCTIVE]),
    f"{RELATIVE_SENTENCE}.adjectival": (RELATIVE_SYNTAX, [RELATIVE, INDICATIVE]),

    "sentence_construction_possibilitites.two_complete_coordinating_sentence.connector_piece": (
        "conjunctions/connective-continuative-coordinate", [INDICATIVE]),
}


def resolve():
    """Every usage path with its two keys, and a report of anything that does not resolve."""
    known_groups = set(all_groups())
    wired, missing = {}, []
    for path, (syntactic, requires, *describe) in WIRING.items():
        if syntactic not in SYNTAX["items"]:
            missing.append(("syntax", path, syntactic))
        for requirement in requires:
            unknown = [g for g in requirement if g not in known_groups]
            if unknown or not requirement:
                missing.append(("grammar", path, unknown or "empty requirement"))
        wired[path] = {"syntactic_item": syntactic, "grammar_requires": requires}
        if describe:
            wired[path]["describe"] = describe[0]
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

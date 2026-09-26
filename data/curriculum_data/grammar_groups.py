"""The grammar a sentence plan is gated on, one level above the slot.

A plan asks whether a student can build a construction at all - can they form an aorist passive
participle - not whether they have met one particular cell of its chart. So a slot key collapses to
its rule: aor1-pas-ptc, pres-act-ind, decl2, article. A rule holds every pattern the grammars print
for it - thematic alongside the contract, liquid and athematic verbs - so the rule is the group.
"""

import collections
from functools import cache

from data.student_data.student_data_helper_functions import load_grammar_scaffolding
from greek_text import fold_greek


def group_of(slot_key):
    """The group a grammar slot belongs to."""
    return slot_key.split("::")[0]


@cache
def all_groups():
    """Every group, in curriculum order."""
    structure = load_grammar_scaffolding()["structure"]
    return sorted(structure, key=lambda rule: int(structure[rule]["sequence"]))


def groups_matching(predicate):
    """The groups whose key satisfies predicate, in curriculum order."""
    return [group for group in all_groups() if predicate(group)]


def group_name(group):
    return load_grammar_scaffolding()["structure"][group]["name"]


def group_examples(group, count):
    """The commonest GNT forms filed under a group's items, each with its lemma."""
    found = collections.Counter()
    for item in load_grammar_scaffolding()["items"].values():
        if item["rule"] == group:
            for form in item["gnt_forms"]:
                found[(form["form"], form["lemma"])] += form["occurrences"]
    examples, seen = [], set()
    for form, lemma in (pair for pair, _ in found.most_common()):
        if fold_greek(form) not in seen:
            seen.add(fold_greek(form))
            examples.append(f"{form} ({lemma})")
    return examples[:count]

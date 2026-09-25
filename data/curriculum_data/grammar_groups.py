"""The grammar a sentence plan is gated on, one level above the slot.

A plan asks whether a student can build a construction at all - can they form an aorist passive
participle - not whether they have met one particular cell of its chart. So a slot key collapses to
its rule: aor1-pas-ptc, pres-act-ind, decl2, article. A rule holds every stem type the grammars
print for it - λύω alongside the contract, liquid and athematic verbs - so the rule is the group.
"""

from functools import cache

from data.student_data.student_data_helper_functions import load_grammar_scaffolding
from text_fabric.corpus_index import load_corpus_index

# How a rule key's parts read as the corpus's tense, voice and mood. The corpus tags some present
# and imperfect forms "middlepassive", which counts toward both.
TENSES = {"pres": "present", "impf": "imperfect", "fut": "future", "aor1": "aorist", "aor2": "aorist",
          "perf": "perfect"}
VOICES = {"act": {"active"}, "mid": {"middle", "middlepassive"}, "pas": {"passive", "middlepassive"}}
MOODS = {"ind": "indicative", "subj": "subjunctive", "inf": "infinitive", "impv": "imperative",
         "ptc": "participle"}


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


def group_frequency(group):
    """How many verbs in the corpus carry this group's tense, voice and mood. A plan weighs the
    charts it could hand over by this, so a construction is built the way the corpus usually builds
    it: a causal infinitive is far likelier to be aorist active than perfect middle. Groups that are
    not verbal, and the εἰμί charts, count as 1."""
    parts = group.split("-")
    if len(parts) != 3 or parts[0] not in TENSES or parts[1] not in VOICES or parts[2] not in MOODS:
        return 1
    counts = load_corpus_index()["morphology"]
    return max(1, sum(counts.get(f"{TENSES[parts[0]]}|{voice}|{MOODS[parts[2]]}", 0)
                      for voice in VOICES[parts[1]]))


def group_chart(group):
    """The forms of one group as the charts print them, one entry per paradigm, labelled with the
    verb and its stem type where the chart names them: {label: {parsing: form}}."""
    scaffolding = load_grammar_scaffolding()
    chart = {}
    for paradigm in scaffolding["structure"][group]["paradigms"].values():
        label = paradigm["lexical_form"]
        if paradigm.get("lemma"):
            label += f" ({paradigm['lemma']}, {paradigm['stem_class']})"
        chart[label] = {scaffolding["items"][slot]["parsing"]: scaffolding["items"][slot]["form"]
                        for slot in paradigm["slots"] if slot in scaffolding["items"]}
    return chart

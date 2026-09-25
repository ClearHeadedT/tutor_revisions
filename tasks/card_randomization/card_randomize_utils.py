"""Builds the sentence plan a card is written to.

The plan fixes what code can decide well and leaves the rest to the model. Code decides:

  the shape of the sentence   drawn from the traversal, gated by what the student has learned -
                              the construction's syntactic category, and the grammar group it is
                              built from - and handed over with its formation notes and the
                              paradigm chart it needs, so the model builds from the grammars'
                              forms rather than its own recollection
  anything extra to include   drawn from the syntax items the student has learned
  the settings on offer       two everyday situations from the scene bank, matched to a
                              vocabulary item's Louw-Nida domain where the bank allows

The model decides everything that needs knowledge of Greek to decide: the verb, what goes with
it, and how the scene plays out inside the setting it picks. Choosing those in code produced
sentences that were grammatical on paper and nonsensical in fact; see the audit that led here.

Nothing here raises on a student who has learned little. Every draw falls back to something
simpler - a single main clause, no extras - which is an ordinary outcome early in the curriculum.
"""

import random
import re

from data.curriculum_data.curriculum_helper_functions import load_scene_bank
from data.curriculum_data.grammar_groups import group_chart, group_frequency, group_name, group_of
from data.student_data.student_data_helper_functions import (
    load_grammar_scaffolding,
    load_syntax_scaffolding,
    load_vocabulary_scaffolding,
)
from tasks.card_randomization.card_randomize_constants import (
    CATEGORY_WEIGHTS,
    EXTRA_CHANCE,
    LEVEL_PLANS,
    PLAIN_CARD_TYPES,
    SENTENCE_TYPE_WEIGHTS,
    SETTING_OPTIONS,
)
from tasks.card_randomization.card_randomize_traversal import traversal
from tasks.card_randomization.formation_instructions import formation_instructions
from tasks.new_card_creation.utils import unpack_syntactic_item

SENTENCES_KEY = "sentence_construction_possibilitites"
SIMPLE = "simple_beginner_sentence"

SHAPE_NAMES = {
    SIMPLE: "a single main clause",
    "main_and_dependent_sentence": "a main clause with an adverbial dependent clause",
    "main_and_relative_sentence": "a main clause with a relative clause",
    "two_complete_coordinating_sentence": "two independent clauses joined by a coordinating conjunction",
}

# Syntax roots whose members are one category for the purpose of "do not put a second instance of
# it in the sentence". Elsewhere the category is the first two segments of the key, since roots such
# as moods or conjunctions hold unrelated constructions.
WHOLE_ROOTS = {"nominative", "vocative", "genitive", "dative", "accusative",
               "participle", "infinitive", "conditional-sentences", "prepositions"}


def weighted_choice(names, weights):
    """One name from the list, drawn against the weights table in the constants.

    Returns None on an empty list. Nothing being available is an ordinary state for a student
    early in the curriculum, not an error - the caller falls back to a simpler card."""
    if not names:
        return None
    return random.choices(names, weights=[weights.get(name, 0.1) for name in names], k=1)[0]


def ranked_choice(names):
    """One name, the earlier entries likelier. The order written into the traversal
    is the order of preference. Returns None when there is nothing to choose from."""
    if not names:
        return None
    return random.choices(names, weights=range(len(names), 0, -1), k=1)[0]


def sample_up_to(items, wanted):
    """As many as asked for, or all of them when there are fewer than that."""
    return random.sample(items, k=min(wanted, len(items)))


def syntax_category(key):
    """The category a syntax key belongs to, for keeping two of one kind out of a sentence."""
    segments = key.split("/")
    return segments[0] if segments[0] in WHOLE_ROOTS else "/".join(segments[:2])


# ---- the sentence's shape ---------------------------------------------------------------------

def is_usage(node):
    return isinstance(node, dict) and "syntactic_item" in node


def options(node):
    """A node's choices: its usages where it has them, otherwise its child categories."""
    if "usages" in node:
        return node["usages"]
    return {name: child for name, child in node.items() if isinstance(child, dict) and name != "position"}


def any_available(node, available):
    """True when anything at or under this node is a usage the student can take."""
    if is_usage(node):
        return available(node)
    return isinstance(node, dict) and any(any_available(child, available) for child in options(node).values())


def usage_available(usage, student, groups, blocked):
    """A usage is open when the student has met its syntactic category and at least one group
    from each grammar requirement, and its category is not one the sentence must keep out."""
    return (usage["syntactic_item"] in student.syntax
            and syntax_category(usage["syntactic_item"]) not in blocked
            and all(any(group in groups for group in requirement)
                    for requirement in usage["grammar_requires"]))


def choose_shape(student, groups, blocked):
    """A path through the traversal to one usage, or SIMPLE."""
    sentences = traversal[SENTENCES_KEY]
    available = lambda usage: usage_available(usage, student, groups, blocked)
    types = [name for name, node in sentences.items() if name == SIMPLE or any_available(node, available)]
    sentence_type = weighted_choice(types, SENTENCE_TYPE_WEIGHTS) or SIMPLE
    if sentence_type == SIMPLE:
        return [SIMPLE], None, None
    path, node, position = [sentence_type], sentences[sentence_type], None
    while not is_usage(node):
        position = node.get("position", position)
        choices = {name: child for name, child in options(node).items() if any_available(child, available)}
        name = ranked_choice(list(choices)) if "usages" in node else weighted_choice(list(choices), CATEGORY_WEIGHTS)
        path.append(name)
        node = choices[name]
    return path, node, node.get("position", position)


def describe_syntax(key):
    """A syntax item as the model reads it: what the usage is called, where it sits in the grammars'
    taxonomy, and its definition, marked as a syntactic explanation. The definitions are GGBB's
    one-line summaries, which read as fragments on their own; the frame around them says what they
    are."""
    unpacked = unpack_syntactic_item(key)
    names = [node.get("display_name") for node in unpacked["ancestors"] if node.get("display_name")]
    text = f"{unpacked['item'].get('display_name')} - a syntactic usage"
    if names:
        text += f", under {' > '.join(names)}"
    description = unpacked["item"].get("description")
    if description:
        # one description still carries a page marker from the grammar it was extracted from
        description = re.sub(r"\s+", " ", re.sub(r"\s+p \d+\s+", " ", description)).strip()
        text += f". Syntactic explanation: {description}"
    return text + "."


def formation_notes(path_key):
    """formation, function and note for a traversal path. example_ref is left out: a verse
    pointer invites the model to recall the verse, which is what a card must not do."""
    entry = formation_instructions.get(path_key, {})
    return {field: entry[field] for field in ("formation", "function", "note") if entry.get(field)}


def describe_position(position):
    if not position or position.get("default") == "split":
        return None
    return (f"{position['default']} the main clause by default; "
            f"{position['marked']} it when you mean to give it emphasis")


def shape_block(path, usage, position, groups):
    """The sentence shape, rendered for the model."""
    path_key = ".".join([SENTENCES_KEY] + path)
    shape = SHAPE_NAMES[path[0]]
    if len(path) > 1:
        detail = [step.replace("_", " ") for step in path[1:] if step not in ("adverbial", "connector_piece")]
        if detail:
            shape += ": " + ", ".join(detail)
    block = {"shape": shape, **formation_notes(path_key)}
    if usage is None:
        return block
    described = usage.get("describe", usage["syntactic_item"])
    if described:
        block["syntactic_category"] = describe_syntax(described)
    where = describe_position(position)
    if where:
        block["position"] = where
    # One chart, for the form the construction turns on: the participle, the infinitive, the
    # relative pronoun, the subjunctive, drawn in proportion to how often the corpus uses it. A construction that takes any indicative at all turns on
    # its conjunction, not a form, so a chart of one tense picked at random would only mislead.
    requirement = usage["grammar_requires"][0]
    any_indicative = all(g.endswith("-ind") for g in requirement) and any(g.startswith("pres-") for g in requirement)
    if not any_indicative:
        candidates = [g for g in requirement if g in groups]
        group = random.choices(candidates, weights=[group_frequency(g) for g in candidates], k=1)[0]
        block["paradigm"] = {"name": group_name(group), "forms": group_chart(group)}
    return block


# ---- extras -----------------------------------------------------------------------------------

def choose_extras(student, count, blocked):
    """Up to count syntax items the student has learned, no two of one category, none of a
    category the sentence already carries."""
    items = load_syntax_scaffolding()["items"]
    extras, taken = [], set(blocked)
    candidates = [key for key in student.syntax if key in items]
    random.shuffle(candidates)
    for key in candidates:
        if len(extras) == count:
            break
        if syntax_category(key) in taken:
            continue
        taken.add(syntax_category(key))
        extras.append(describe_syntax(key))
    return extras


# ---- settings ---------------------------------------------------------------------------------

def choose_settings(ln_domain=None, avoid=()):
    """SETTING_OPTIONS settings from the scene bank, as {id: scene}. Those sharing the item's
    Louw-Nida domain come first; the rest are made up at random. Settings the item's recent cards
    used are passed over."""
    bank = [scene for scene in load_scene_bank()["scenes"] if scene["id"] not in avoid]
    matching = [scene for scene in bank if ln_domain and ln_domain in scene["ln_domains"]]
    chosen = sample_up_to(matching, SETTING_OPTIONS)
    rest = [scene for scene in bank if scene not in chosen]
    chosen += sample_up_to(rest, SETTING_OPTIONS - len(chosen))
    return {scene["id"]: scene["scene"] for scene in chosen}


# ---- the plan ---------------------------------------------------------------------------------

def target_constraints(target_domain, target_key):
    """What the card's own item rules out of the rest of the sentence, and the Louw-Nida domain
    its settings should share.

    A grammar card may not carry a second form of its own group (a second article on an article
    card), nor a second use of its case. A syntax card may not carry a second instance of its own
    category."""
    blocked_groups, blocked_categories, ln_domain = set(), set(), None
    if target_domain == "grammar":
        blocked_groups.add(group_of(target_key))
        case = load_grammar_scaffolding()["items"][target_key].get("features", {}).get("case")
        if case:
            blocked_categories.add(case)
    elif target_domain == "syntax":
        blocked_categories.add(syntax_category(target_key))
    elif target_domain == "vocabulary":
        ln_domain = (load_vocabulary_scaffolding()["items"].get(target_key) or {}).get("domain")
    return blocked_groups, blocked_categories, ln_domain


def build_sentence_plan(student, card_type, target_domain, target_key):
    """The plan for one card. target_domain is "vocabulary", "grammar" or "syntax", and
    target_key the item's key in that domain's scaffolding."""
    blocked_groups, blocked, ln_domain = target_constraints(target_domain, target_key)
    level = LEVEL_PLANS.get(student.level, LEVEL_PLANS["beyond_beginner"])
    plain = card_type in PLAIN_CARD_TYPES
    groups = set(student.grammar_groups_learned()) - blocked_groups

    if level["shape"] and not plain:
        path, usage, position = choose_shape(student, groups, blocked)
    else:
        path, usage, position = [SIMPLE], None, None
    if usage is not None:
        blocked = blocked | {syntax_category(usage["syntactic_item"])}

    extras = []
    if not plain:
        count = sum(random.random() < EXTRA_CHANCE for _ in range(level["extras"]))
        extras = choose_extras(student, count, blocked)

    return {
        "sentence_shape": shape_block(path, usage, position, groups),
        "also_include": extras,
        "setting_options": choose_settings(ln_domain, avoid=student.recent_settings(target_key)),
    }

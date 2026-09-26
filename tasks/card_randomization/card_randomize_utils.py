"""Builds the sentence plan a card is written to: its shape, drawn by how regular each
construction is and gated by what the student has learned, or the item's own construction where
it is one; an optional extra usage to pick from three; and two settings. The model chooses every
word."""

import random
import re

from data.curriculum_data.curriculum_helper_functions import load_scene_bank
from data.curriculum_data.grammar_groups import group_examples, group_name, group_of
from data.student_data.student_data_helper_functions import (
    load_grammar_scaffolding,
    load_syntax_scaffolding,
    load_vocabulary_scaffolding,
)
from tasks.card_randomization.card_randomize_constants import (
    EXTRA_CHANCE,
    EXTRA_OPTIONS,
    FREQUENCY_NOTES,
    GRAMMAR_EXAMPLES,
    HOSTED_GROUPS,
    LEVEL_PLANS,
    MAIN_CLAUSE_GROUPS,
    PLAIN_CARD_TYPES,
    SENTENCE_TYPE_WEIGHTS,
    SETTING_OPTIONS,
    TIER_WEIGHTS,
    USAGE_TIERS,
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


def grammar_known(usage, groups):
    """True when the student has at least one group from each of the usage's grammar requirements."""
    return all(any(group in groups for group in requirement) for requirement in usage["grammar_requires"])


def usage_available(usage, student, groups, blocked):
    """A usage is open when the student has met its syntactic category and the grammar it needs,
    and its category is not one the sentence must keep out."""
    return (usage["syntactic_item"] in student.syntax
            and syntax_category(usage["syntactic_item"]) not in blocked
            and grammar_known(usage, groups))


def builds(usage, syntax_key):
    """True when a usage builds the syntax item, a usage under it, or the usage it falls under."""
    built = usage.get("describe", usage["syntactic_item"])
    return bool(built) and (built == syntax_key or built.startswith(syntax_key + "/")
                            or syntax_key.startswith(built + "/"))


def usage_tier(path):
    return USAGE_TIERS.get(".".join(path), "regular")


def best_weight(node, path, available):
    """A category weighs as much as its most regular open usage."""
    if is_usage(node):
        return TIER_WEIGHTS[usage_tier(path)] if available(node) else 0
    return max((best_weight(child, path + [name], available) for name, child in options(node).items()), default=0)


def choose_shape(available, simple):
    """A path through the traversal to one usage that passes available, or SIMPLE. simple says
    whether a single main clause is one of the choices; it is the fallback either way."""
    sentences = traversal[SENTENCES_KEY]
    types = [name for name, node in sentences.items()
             if (name == SIMPLE and simple) or any_available(node, available)]
    sentence_type = weighted_choice(types, SENTENCE_TYPE_WEIGHTS) or SIMPLE
    if sentence_type == SIMPLE:
        return [SIMPLE], None, None
    path, node, position = [sentence_type], sentences[sentence_type], None
    while not is_usage(node):
        position = node.get("position", position)
        weights = {name: best_weight(child, path + [name], available) for name, child in options(node).items()}
        name = weighted_choice([name for name, weight in weights.items() if weight], weights)
        path.append(name)
        node = options(node)[name]
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


def shape_block(path, usage, position, groups, target_group=None):
    """The sentence shape, rendered for the model. target_group is the grammar item's own group
    when the shape was chosen to carry it."""
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
    tier = usage_tier(path)
    if tier in FREQUENCY_NOTES:
        block["frequency"] = FREQUENCY_NOTES[tier]
    # A construction taking any indicative turns on its conjunction, not on a form.
    requirement = usage["grammar_requires"][0]
    if target_group in requirement:
        block["grammar_options"] = [{"option": f"{group_name(target_group)}, the item under review: "
                                               "build the construction on its target form"}]
    elif not (all(g.endswith("-ind") for g in requirement) and any(g.startswith("pres-") for g in requirement)):
        block["grammar_options"] = grammar_options([g for g in requirement if g in groups])
    return block


def grammar_options(groups):
    """The forms the construction can take that the student has learned, each with its commonest
    GNT forms. First and second aorist are one option."""
    found = {}
    for group in groups:
        name = group_name(group).replace("First ", "").replace("Second ", "")
        if name not in found:
            found[name] = group_examples(group, GRAMMAR_EXAMPLES)
    return [{"option": name, "gnt_examples": examples} if examples else {"option": name}
            for name, examples in found.items()]


# ---- extras -----------------------------------------------------------------------------------

def extra_options(student, blocked):
    """EXTRA_OPTIONS syntax items the student has learned for the model to pick one from, drawn by
    how widely the grammars teach them, no two of one category and none the sentence already has."""
    items = load_syntax_scaffolding()["items"]
    candidates = [key for key in student.syntax if key in items and syntax_category(key) not in blocked]
    chosen = []
    while candidates and len(chosen) < EXTRA_OPTIONS:
        key = random.choices(candidates, weights=[TIER_WEIGHTS[items[k].get("tier", "regular")] for k in candidates])[0]
        candidates = [k for k in candidates if syntax_category(k) != syntax_category(key)]
        text = describe_syntax(key)
        note = FREQUENCY_NOTES.get(items[key].get("tier"))
        chosen.append(f"{text} {note}" if note else text)
    return chosen


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


def shape_source(student, target_domain, target_key, groups, blocked):
    """What the shape is drawn from: a test each usage must pass, whether a single main clause is
    one of the choices, and the grammar item's own group when the shape is built on it.

    Where the item is itself a construction, the shape is that construction. A syntax item the
    traversal builds - a conditional, a purpose infinitive, a relative clause - is the shape. A form
    a main clause cannot carry by itself - a subjunctive, a relative pronoun, a participle or
    infinitive that does not stand in the main clause - is built on a construction that takes it.
    Anything else fits in any clause, and the shape is drawn from outside the item's own category."""
    if target_domain == "syntax":
        def own(usage):
            return builds(usage, target_key)
        if any_available(traversal[SENTENCES_KEY], own):
            return (lambda usage: own(usage) and grammar_known(usage, groups)), False, None
    if target_domain == "grammar" and group_of(target_key).endswith(HOSTED_GROUPS):
        group = group_of(target_key)
        def takes_target(usage):
            return (any(group in requirement for requirement in usage["grammar_requires"])
                    and usage_available(usage, student, groups | {group}, blocked))
        return takes_target, group.endswith(MAIN_CLAUSE_GROUPS), group
    return (lambda usage: usage_available(usage, student, groups, blocked)), True, None


def build_sentence_plan(student, card_type, target_domain, target_key):
    """The plan for one card. target_domain is "vocabulary", "grammar" or "syntax", and
    target_key the item's key in that domain's scaffolding."""
    blocked_groups, blocked, ln_domain = target_constraints(target_domain, target_key)
    level = LEVEL_PLANS.get(student.level, LEVEL_PLANS["beyond_beginner"])
    plain = card_type in PLAIN_CARD_TYPES
    groups = set(student.grammar_groups_learned()) - blocked_groups
    available, simple, target_group = shape_source(student, target_domain, target_key, groups, blocked)

    if level["shape"] and not plain:
        path, usage, position = choose_shape(available, simple)
    else:
        path, usage, position = [SIMPLE], None, None
    if usage is not None:
        blocked = blocked | {syntax_category(usage["syntactic_item"])}

    plan = {"sentence_shape": shape_block(path, usage, position, groups, target_group)}
    if level["extra"] and not plain and random.random() < EXTRA_CHANCE:
        plan["also_include_one_of"] = extra_options(student, blocked)
    plan["setting_options"] = choose_settings(ln_domain, avoid=student.recent_settings(target_key))
    return plan

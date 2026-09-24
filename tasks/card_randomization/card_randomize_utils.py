from data.curriculum_data.curriculum_helper_functions import (
    load_card_randomizer_elements,
    load_vocabulary_items,
)
from data.student_data.student import Student
from tasks.card_randomization.card_randomize_traversal import traversal
from tasks.card_randomization.card_randomize_constants import (
    SENTENCE_TYPE_WEIGHTS,
    ADVERBIAL_DEPENDENT_CATEGORIES,
    VERB_USAGE_WEIGHTS,
)
from tasks.card_randomization.formation_instructions import formation_instructions
import random


def traverse_probability_card_randomizer(student_id="austin"):
    student_class = Student(student_id=student_id)
    match student_class.level:
        case "beginner":
            return beginner_traversal(student_class=student_class)

        case "beyond_beginner":
            return beyond_beginner_traversal(student_class=student_class)

        case "advanced":
            raise NotImplementedError


def beginner_traversal(student_class):
    """One main clause: a verb the student knows, with partners drawn against it.

    This reads the same pool every other path reads. It used to read `subject_pairings` off the
    traversal, a second shape for the same data that was never filled in."""
    possibilities = lexeme_possibilities_by_key(
        student=student_class, usage_key="sentence_vitals.verb.finite_verb")
    if not possibilities:
        return None
    selection = select_lexemes_for_key(student=student_class, lexical_possibilities=possibilities)
    verb, options = next(iter(selection.items()))
    return format_traversal_elements(
        verb=f"{verb} ({options['gloss']})",
        subjects=options["subject_lexeme_possibilities"],
        objects=options["object_lexeme_possibilities"])



def beyond_beginner_traversal(student_class):
    instructions_key = "sentence_construction_possibilitites."
    sentence_types = traversal['sentence_construction_possibilitites']
    valid_sentence_types = [name for name, node in sentence_types.items()
                            if any_check_traversal_uses_validity(node, student=student_class)]
    sentence_type = weighted_choice(valid_sentence_types, SENTENCE_TYPE_WEIGHTS)
    if sentence_type is None:
        return beginner_traversal(student_class=student_class)
    instructions_key += f"{sentence_type}."
    if sentence_type == "simple_beginner_sentence":
        return beginner_traversal(student_class=student_class)

    elif sentence_type == "main_and_dependent_sentence":
        instructions_key += "adverbial."
        adverbial = sentence_types[sentence_type]["adverbial"]
        valid_categories = [name for name, node in adverbial.items()
                            if any_check_traversal_uses_validity(node, student=student_class)]
        category = weighted_choice(valid_categories, ADVERBIAL_DEPENDENT_CATEGORIES)
        if category is None:
            return beginner_traversal(student_class=student_class)
        instructions_key += f"{category}."
        usages = adverbial[category]["usages"]
        valid_usages = [name for name, usage in usages.items()
                        if check_traversal_specific_uses(usage=usage, student=student_class)]
        usage_name = ranked_choice(valid_usages)
        if usage_name is None:
            return beginner_traversal(student_class=student_class)
        instructions_key += f"{usage_name}"
        usage = usages[usage_name]
        valid_verbal_lexemes = lexeme_possibilities_by_key(student=student_class, usage_key=instructions_key)
        if not valid_verbal_lexemes:
            # No verb this student knows can be built into this clause. A simpler sentence is a
            # better answer than no card at all.
            return beginner_traversal(student_class=student_class)
        lexical_items = select_lexemes_for_key(student=student_class, lexical_possibilities=valid_verbal_lexemes)
        valid_grammar_items = [g_item for g_item in usage['grammatical_items'] if g_item in student_class.grammar]
        grammar_item = ranked_choice(valid_grammar_items)
        instructions = formation_instructions[instructions_key]
        main_clause_vitals = select_sentence_vitals(student_class=student_class)
        dependent_clause_information = {
            "Trajectory of key traced to individual occurrence": instructions_key,
            "Helper instructions for formation": instructions,
            "The specific grammatical item with its morphological specification": grammar_item,
            "Verbal options for sentence formation and their substantive counterparts": lexical_items
        }
        synthesis = {
            "Main clause information": main_clause_vitals,
            "Dependent clause information": dependent_clause_information
        }
        return synthesis

    elif sentence_type == "main_and_relative_sentence":
        instructions_key += "adjectival"
        adjectival = sentence_types[sentence_type]["adjectival"]
        valid_verbal_lexemes = lexeme_possibilities_by_key(student=student_class, usage_key=instructions_key)
        if not valid_verbal_lexemes:
            return beginner_traversal(student_class=student_class)
        lexical_items = select_lexemes_for_key(student=student_class, lexical_possibilities=valid_verbal_lexemes)
        valid_grammar_items = [g_item for g_item in adjectival.get('grammatical_items', []) if g_item in student_class.grammar]
        grammar_item = ranked_choice(valid_grammar_items)
        instructions = formation_instructions[instructions_key]
        relative_paradigm = adjectival.get('relative_paradigm')
        main_clause_vitals = select_sentence_vitals(student_class=student_class)
        relative_clause_information = {
            "Trajectory of key traced to individual occurrence": instructions_key,
            "Helper instructions for formation": instructions,
            "The specific grammatical item with its morphological specification": grammar_item,
            "The relative pronoun paradigm to draw from": relative_paradigm,
            "Verbal options for sentence formation and their substantive counterparts": lexical_items
        }
        synthesis = {
            "Main clause information": main_clause_vitals,
            "Relative clause information": relative_clause_information
        }
        return synthesis

    elif sentence_type == "two_complete_coordinating_sentence":
        raise NotImplementedError





def format_traversal_elements(verb, subjects, objects, additional_elements="None"):
    formatted_string = (
        f"The verb that sets sentence, subject, and object context: {verb}\n"
        f"Subject options: {subjects}\n"
        f"Object options: {objects}\n"
        f"Additional elements for inclusion (if applicable): {additional_elements}\n"
    )
    return formatted_string


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
    """As many as asked for, or all of them when the student knows fewer than that."""
    return random.sample(items, k=min(wanted, len(items)))


def any_check_traversal_uses_validity(desired_path, student):
    """True when anything anywhere under this node is a usage the student can take."""
    if not isinstance(desired_path, dict):
        return False
    for key, value in desired_path.items():
        if key == "usages":
            if any(check_traversal_specific_uses(usage, student) for usage in value.values()):
                return True
        elif any_check_traversal_uses_validity(value, student):
            return True
    return False


def check_traversal_specific_uses(usage, student):
    """One usage is available when the student has met one of its grammatical forms and
    the syntactic category it sits under. A usage carrying neither yet is unavailable,
    which is how the empty placeholders in the traversal read today."""
    if not isinstance(usage, dict):
        return False
    grammatical_items = usage.get("grammatical_items") or []
    syntactic_item = usage.get("syntactic_item")
    if not grammatical_items or not syntactic_item:
        return False
    return (any(g_item in student.grammar for g_item in grammatical_items)
            and syntactic_item in student.syntax)


# What a realization needs of a verb. A participial clause can only be built from a verb the
# corpus attests as a participle - 5 of the 222 in the pool never appear as one - so the filter
# runs before the draw rather than discovering the problem after it.
REQUIRED_MOOD = {
    "adverbial_participle": "participle",
    "substantival_participle": "participle",
    "infinitive": "infinitive",
    "articular_infinitive": "infinitive",
    "substantival_infinitive": "infinitive",
    "finite_with_infinitive_complement": "infinitive",
    "hina_subjunctive": "subjunctive",
    "third_class": "subjunctive",
    "subjunctive": "subjunctive",
}
# How many partners a verb needs before it is worth offering, and how many of each to hand over.
MIN_PARTNERS = 2
OPTIONS_PER_SLOT = 3
VERB_OPTIONS = 1


def lexeme_possibilities_by_key(student, usage_key):
    """The verbs this student could build this usage from, with their attested partners.

    Three filters, in order: the student has met the verb, the corpus attests the verb in the
    mood this realization needs, and enough of its partners are words the student also knows.
    Returns an empty dict rather than None when nothing survives - the caller decides whether
    that is fatal, and for most of them it is not."""
    pool = load_card_randomizer_elements().get("verbs", {})
    needed_mood = REQUIRED_MOOD.get(usage_key.rsplit(".", 1)[-1])
    options = {}
    for lexeme, internals in pool.items():
        if lexeme not in student.vocabulary:
            continue
        if needed_mood and needed_mood not in internals.get("moods", ()):
            continue
        subjects = [w for w in internals["subject_lexemes"] if w in student.vocabulary]
        objects = [w for w in internals["object_lexemes"] if w in student.vocabulary]
        if len(subjects) < MIN_PARTNERS and len(objects) < MIN_PARTNERS:
            continue
        options[lexeme] = {**internals,
                           "subject_lexemes": subjects, "object_lexemes": objects}
    return options


def select_lexemes_for_key(student, lexical_possibilities):
    """One verb, and several partners drawn against it.

    The verb is fixed rather than varied because it decides both the shape of the clause and
    what will sit in it coherently. Offering three verbs alongside three subjects and three
    objects gives the model twenty-seven combinations, most of which pair words that never go
    together; offering one verb and three of everything else gives it options that all work."""
    if not lexical_possibilities:
        return {}
    chosen = sample_up_to(list(lexical_possibilities), VERB_OPTIONS)
    options = {}
    for lexeme in chosen:
        internals = lexical_possibilities[lexeme]
        options[lexeme] = {
            "gloss": internals.get("gloss"),
            "semantic_domain": internals.get("domain"),
            "object_case": (internals.get("government") or {}).get("case"),
            "attested_prepositions": internals.get("prepositions", []),
            "subject_lexeme_possibilities": sample_up_to(
                internals["subject_lexemes"], OPTIONS_PER_SLOT),
            "object_lexeme_possibilities": sample_up_to(
                internals["object_lexemes"], OPTIONS_PER_SLOT),
        }
    return options


def select_sentence_vitals(student_class):
    verbal_usages = traversal['sentence_vitals']['verb']['usages']
    valid_verbal_categories = [name for name, node in verbal_usages.items()
                        if check_traversal_specific_uses(usage=node, student=student_class)]
    verbal_category = weighted_choice(valid_verbal_categories, VERB_USAGE_WEIGHTS) or "finite_verb"
    verbal_grammar_item_possibilities = [g_item for g_item in verbal_usages[verbal_category]['grammatical_items'] if g_item in student_class.grammar]
    verbal_grammar_item = ranked_choice(verbal_grammar_item_possibilities)
    lexical_options = lexeme_possibilities_by_key(student=student_class, usage_key=f"sentence_vitals.verb.{verbal_category}")
    if not lexical_options:
        # Fall back to a plain finite verb, which every student who has met one can build.
        lexical_options = lexeme_possibilities_by_key(
            student=student_class, usage_key="sentence_vitals.verb.finite_verb")
    lexical_items = select_lexemes_for_key(student=student_class, lexical_possibilities=lexical_options)
    valid_subject_categories = [name for name, node in traversal['sentence_vitals']['subject']['usages'].items()
                                if check_traversal_specific_uses(usage=node, student=student_class)]
    subject_category = ranked_choice(names=valid_subject_categories)
    subject_formation_instructions = formation_instructions.get(f"sentence_vitals.subject.{subject_category}")
    valid_object_categories = [name for name, node in traversal['sentence_vitals']['object']['usages'].items()
                                if check_traversal_specific_uses(usage=node, student=student_class)]
    object_category = ranked_choice(names=valid_object_categories)
    object_formation_instructions = formation_instructions.get(f"sentence_vitals.object.{object_category}")
    synthesis = {
        "Verb lexical options for sentence formation and their substantive counterparts": lexical_items,
        "Verb morphological and grammatical parsing information": verbal_grammar_item,
        "The specific syntactic usage of the verb": verbal_category,
        "The specific syntactic usage of the subject": subject_category,
        "Instructions for subject grammatical formation (if applicable)": subject_formation_instructions,
        "The specific syntactic usage of the object": object_category,
        "Instructions for object grammatical formation (if applicable)": object_formation_instructions
    }
    return synthesis


def vocabulary_item_entry(student_class, vocabulary_item):
    """Builds a card around one review item, placed in the slot it naturally occupies.

    A word's natural frame is the (role, case) the corpus actually puts it in - pistis is an
    instrumental dative far more often than anything else, anthropos a nominative subject. Using
    it beats assigning a slot at random: the item lands where Greek puts it, and the rest of the
    sentence is built around it rather than bent to accommodate it.

    Returns None when nothing can be built, which the caller reads as "fall back to a simpler
    card" rather than as an error."""
    vocabulary = load_vocabulary_items()
    entry = vocabulary.get(vocabulary_item if isinstance(vocabulary_item, str)
                           else vocabulary_item.get("key"))
    if entry is None:
        return None

    pool = load_card_randomizer_elements()
    if entry["part_of_speech"] == "verb":
        # A verb sets the frame itself, so it simply takes the place of the drawn verb.
        internals = pool.get("verbs", {}).get(entry["key"])
        if not internals:
            return None
        subjects = [w for w in internals["subject_lexemes"] if w in student_class.vocabulary]
        objects = [w for w in internals["object_lexemes"] if w in student_class.vocabulary]
        return {
            "review_item": entry["key"],
            "role_in_sentence": "verb",
            "semantic_domain": internals.get("domain"),
            "Verb lexical options for sentence formation and their substantive counterparts": {
                entry["key"]: {
                    "gloss": internals.get("gloss"),
                    "object_case": (internals.get("government") or {}).get("case"),
                    "attested_prepositions": internals.get("prepositions", []),
                    "subject_lexeme_possibilities": sample_up_to(subjects, OPTIONS_PER_SLOT),
                    "object_lexeme_possibilities": sample_up_to(objects, OPTIONS_PER_SLOT),
                }},
        }

    # A substantive needs a verb to hang off. Prefer the verbs that actually take it, then any
    # verb sharing its domain; 96% of substantives have at least one such parent.
    frame = (entry.get("natural_frame") or [{}])[0]
    parents = [lexeme for lexeme, internals in pool.get("verbs", {}).items()
               if lexeme in student_class.vocabulary
               and (entry["key"] in internals["subject_lexemes"]
                    or entry["key"] in internals["object_lexemes"])]
    if not parents:
        parents = [lexeme for lexeme, internals in pool.get("verbs", {}).items()
                   if lexeme in student_class.vocabulary
                   and internals.get("domain") == entry.get("domain")]
    if not parents:
        return None
    verb = random.choice(parents)
    internals = pool["verbs"][verb]
    return {
        "review_item": entry["key"],
        "role_in_sentence": frame.get("role") or "unattested",
        "case_it_normally_takes": frame.get("case"),
        "semantic_domain": entry.get("domain"),
        "Verb lexical options for sentence formation and their substantive counterparts": {
            verb: {
                "gloss": internals.get("gloss"),
                "object_case": (internals.get("government") or {}).get("case"),
                "attested_prepositions": internals.get("prepositions", []),
                "subject_lexeme_possibilities": sample_up_to(
                    [w for w in internals["subject_lexemes"]
                     if w in student_class.vocabulary], OPTIONS_PER_SLOT),
                "object_lexeme_possibilities": sample_up_to(
                    [w for w in internals["object_lexemes"]
                     if w in student_class.vocabulary], OPTIONS_PER_SLOT),
            }},
    }


# Some cleanup and building for later:
    # Make JSON of verbals and their substantive counterparts
        # Do this per category. Certain syntactic sentence constructions favor certain items.
    # Make functionality for syntactic variability 
        # More applicable for some than others 
            # Some categories themselves are already syntactic by nature (e.g. adverbial causal participle)
            # Other categories will have syntactic variability in them like genitive
        # REVISION ON THIS -------------
            # Thinking about this a little more, I think simply adding relevant syntactic categories as the baseline is best
                # Genitive, dative, etc need filling out of specific syntactic usages 

    # THEN Functionality to check, based on vocabulary study input, what categories are even valid accordingly
        # Alongside of limited based on vocabulary student familiarity, student syntactic categories known, grammar items known
            # Limit/reduce options - verbal-substantive items returned (for both main and subsidiary pieces) within those limits AND extra pieces that fit (numerically 3?4?) under the semantic domain, too




# Need to formulate the "entry point"
# Should have to initially analyze what it's handed
    # The piece needs to set the lexical/semantic domain and tone
    # Replace any element that normally would be included in the process 
# Cases:
    # Verb
        # Easiest in theory 
        # Verbal item sets the semantic tone - other pieces fall into place accordingly 
        # One potential issue - if the lexical item being studied doesn't fall squarely in the actual verbal-substantive pool
            # Handle it on a case-by-case basis? 
            # For verbals that match - handle it normally 
            # For verbals that don't 
                # Use it as a subsidary piece in dependent?
                    # Then there's the issue of it not matching anything 
                    # Hand it more verbals (10x) than normal to see what is most coherent contextually? 
                        # Only issue here is vast amount of information handed to it (most of it unused)
                
    # Substantive/nominal
        # Find the verbal parallels it sits under (semantic match from verbal parent)
            # Give verbal options? 
            # Again the issue - what about the case where there are no matching overarching verbal parents? 
                # This might be easier here since it can either be object or subject, more occurrences slightly 

    # Everything else?


# Possible solutions:
    # Ensure every vocabulary has at least one parent 
        # Is this even possible? 
            # The verbals are the issue - we're looking for the 200ish that contain relevant matching substantives 
            # How can every substantive fit this bill? Have to stretch the semantic domain (higher distance numerically between verb-subs), but worth a shot?
        # Every substantive to 10 occurrences sits under a verbal umbrella 
    # Some ways of mitigating semantically nonsensical cards with this method:
        # Two methods/pools
            # (1) The conventional way when everything matches nicely - 200ish verbals connected to substantive, reliable counterparts
            # (2) Another pool based on the vocabulary that don't fit neatly 
                # Only utilize this newmethod when necessary - opt for the traditional path/pool
                # Hand-catered verbals/substantives for down to 10 occurrences 
                    # Limited in:
                        # pos usage?
                        # sentence variety/inclusion possibility? 
                            # (this would be because the other pieces fit under the conventional semantic domain pattern)
                            # Just keep it an adverbial modifier? Something generic like causal or purpose
    # Just utilizing text fabric for every call of card creation 
        # Obvious problems:
            # A bit more subjective and hard to keep consistent 
            # Potential for drift of quality
        # Built in functions to analyze semantic domain of lexical item 
            # Random returns based not from JSON, but from text-fabric functionality and other functions that return its result
            # Likely return more options for vital items
            # Same functionality for randomization elements 






# The assumption is that the scaffolding for the actual items inside the dict
# values (currently empty) in the scaffolding will have some information -
# one k-v pair of grammatical_items (the grammar item parallel key, traceable to student progress through the object,
# verifying if it's usable as an option upon initial checks). One k-v pair of syntactic_item (signifying the syntax item
# by key so it can be checked if the student has learned it yet or not similarly). So for a usage to be valid, the
# student has to already have studied the syntactic category broadly and already seen the specific form in grammatical_items.
# Lastly and importantly, one work in progress in having a fairly thorough list of lexical possiblities, likely another
# JSON, which is empty for now but I've loaded load_card_randomizer_elements. It's highly-catered vocabulary for each
# category. I'm still developing the functionality, but it will be utilizing text-fabric to find where particular lexical
# items occur under specific categories. The lexical items in each of these usages will likely be derived from a large pool
# of subjects, verbs, and objects. The subjects and objects are matched and compared against the semantic ln domain of the
# verb for semantic coherence. This portion is undeveloped, but that's the idea.


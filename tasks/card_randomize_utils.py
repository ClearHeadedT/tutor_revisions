from data.curriculum_data.curriculum_helper_functions import load_card_randomizer_elements
from data.student_data.student import Student
from tasks.card_randomize_traversal import traversal
from tasks.card_randomize_constants import SENTENCE_TYPE_WEIGHTS, ADVERBIAL_DEPENDENT_WEIGHTS
from tasks.formation_instructions import formation_instructions
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
    randomize_scaffolding = traversal
    sentence_type = randomize_scaffolding['sentence_construction_possibilitites']['simple_beginner_sentence']
    if 'verbs' not in sentence_type:
        raise NotImplementedError("simple_beginner_sentence has no verbs filled in yet")
    student_known_verbs = [verb for verb in sentence_type['verbs'] if verb in student_class.vocabulary]
    verb = random.choice(student_known_verbs)
    student_known_subjects = [subject for subject in sentence_type['verbs'][verb]['subject_pairings'] if subject in student_class.vocabulary]
    subject_options = sample_up_to(student_known_subjects, 4)
    student_known_objects = [object for object in sentence_type['verbs'][verb]['object_pairings'] if object in student_class.vocabulary]
    object_options = sample_up_to(student_known_objects, 4)
    return format_traversal_elements(verb=verb, subjects=subject_options, objects=object_options)


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

def beyond_beginner_traversal(student_class):
    instructions_key = "sentence_construction_possibilitites."
    sentence_types = traversal['sentence_construction_possibilitites']
    valid_sentence_types = [name for name, node in sentence_types.items()
                            if any_check_traversal_uses_validity(node, student=student_class)]
    sentence_type = weighted_choice(valid_sentence_types, SENTENCE_TYPE_WEIGHTS)
    instructions_key += f"{sentence_type}."
    if sentence_type == "simple_beginner_sentence":
        return beginner_traversal(student_class=student_class)

    elif sentence_type == "main_and_dependent_sentence":
        instructions_key += "adverbial."
        adverbial = sentence_types[sentence_type]["adverbial"]
        valid_categories = [name for name, node in adverbial.items()
                            if any_check_traversal_uses_validity(node, student=student_class)]
        category = weighted_choice(valid_categories, ADVERBIAL_DEPENDENT_WEIGHTS)
        instructions_key += f"{category}."
        usages = adverbial[category]["usages"]
        valid_usages = [name for name, usage in usages.items()
                        if check_traversal_specific_uses(usage=usage, student=student_class)]
        usage_name = ranked_choice(valid_usages)
        instructions_key += f"{usage_name}"
        usage = usages[usage_name]
        valid_verbal_lexemes = lexeme_possibilities_by_key(student=student_class, usage_key=instructions_key)
        if not valid_verbal_lexemes or len(valid_verbal_lexemes) < 5:
            raise ValueError("Error: Likely not enough lexical options available")
        lexical_items = select_lexemes_for_key(student=student_class, lexical_possibilities=valid_verbal_lexemes)
        valid_grammar_items = [g_item for g_item in usage['grammatical_items'] if g_item in student_class.grammar]
        grammar_item = ranked_choice(valid_grammar_items)
        instructions = formation_instructions[instructions_key]
        synthesis = {
            "Trajectory of key traced to individual occurrence": instructions_key,
            "Helper instructions for formation": instructions,
            "The specific grammatical  item with its morphological specification": grammar_item,
            "Verbal options for sentence formation and their substantive counterparts": lexical_items
        }
        return synthesis

    elif sentence_type == "main_and_relative_sentence":
        raise NotImplementedError

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
    """One name from the list, drawn against the weights table in the constants."""
    if not names:
        raise ValueError("Nothing available to choose from for this student")
    return random.choices(names, weights=[weights[name] for name in names], k=1)[0]


def ranked_choice(names):
    """One name, the earlier entries likelier. The order written into the traversal
    is the order of preference."""
    if not names:
        raise ValueError("Nothing available to choose from for this student")
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


def lexeme_possibilities_by_key(student, usage_key):
    lexical_scaffolding = load_card_randomizer_elements()
    lexical_options = {}
    for lexeme, internals in lexical_scaffolding.get(usage_key, {}).items():
        if (
            len(set(internals["subject_lexemes"]).intersection(student.vocabulary)) >= 5
            and len(set(internals["object_lexemes"]).intersection(student.vocabulary)) >= 5
        ):
            lexical_options[lexeme] = internals
    if len(lexical_options) < 4:
        return None
    return lexical_options


def select_lexemes_for_key(student, lexical_possibilities):
    verbs_by_key = list(lexical_possibilities)
    verbal_lexical_items = sample_up_to(verbs_by_key, 5)
    lexical_options_by_verb = {}
    for v_lexeme in verbal_lexical_items:
        internals = lexical_possibilities[v_lexeme]
        subject_lexeme_possibilities = [lexeme for lexeme in internals["subject_lexemes"] if lexeme in student.vocabulary]
        subject_lexemes = sample_up_to(subject_lexeme_possibilities, 3)
        object_lexeme_possibilities = [lexeme for lexeme in internals["object_lexemes"] if lexeme in student.vocabulary]
        object_lexemes = sample_up_to(object_lexeme_possibilities, 3)
        lexical_options_by_verb[v_lexeme] = {
            "subject_lexeme_possibilities": subject_lexemes,
            "object_lexeme_possibilities": object_lexemes
        }
    return lexical_options_by_verb

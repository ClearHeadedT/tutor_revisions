import json

from greek_text import normalize_greek


def load_grammar_scaffolding():
    """Returns the grammar scaffolding: rule/paradigm structure plus the flat slot items"""
    with open('data/curriculum_data/grammar_scaffolding.json', 'r') as file:
        data = json.load(file)
    return normalize_keys(data)


def load_vocabulary_scaffolding():
    """Returns the vocabulary scaffolding: part-of-speech structure plus the flat word items"""
    with open('data/curriculum_data/vocabulary_scaffolding.json', 'r') as file:
        data = json.load(file)
    return normalize_keys(data)


def load_syntax_scaffolding():
    """Returns the syntax scaffolding: category/broad usage structure plus the flat items"""
    with open('data/curriculum_data/syntax_scaffolding.json', 'r') as file:
        data = json.load(file)
    return normalize_keys(data)


def load_vocabulary_senses():
    """The shared Text-Fabric/Louw-Nida enrichment cache, keyed by lemma. These are
    facts about Greek rather than about any student, so one copy serves everyone.
    The cache builder writes this file."""
    with open('data/curriculum_data/vocabulary_senses.json', 'r') as file:
        data = json.load(file)
    return {normalize_greek(lemma): entry for lemma, entry in data.items()}


def save_vocabulary_senses(senses):
    with open('data/curriculum_data/vocabulary_senses.json', 'w') as file:
        json.dump(senses, file, ensure_ascii=False, indent=2)


def load_student_overview(student_id):
    """The facts about a student that nothing else can derive -- their level above all"""
    with open(f'data/student_data/{student_id}/student_overview.json', 'r') as file:
        return json.load(file)


def save_student_vocabulary_data(student_id, data):
    with open(f'data/student_data/{student_id}/student_vocabulary_data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def save_student_card_data(student_id, data):
    with open(f'data/student_data/{student_id}/student_card_data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def normalize_keys(data):
    """Greek appears in item keys, so every key is normalized on load to keep
    the scaffolding and the student's progress joinable. Returns a new dict,
    leaving the one handed in as it was."""
    return {**data, "items": {normalize_greek(key): item for key, item in data["items"].items()}}


def load_student_grammar_data(student_id):
    """Returns student data from relevant student JSON"""
    with open(f'data/student_data/{student_id}/student_grammar_data.json', 'r') as file:
        data = json.load(file)
    return data


def load_student_vocabulary_data(student_id):
    """Returns the vocabulary for a student based on ID in their respective JSON file"""
    with open(f'data/student_data/{student_id}/student_vocabulary_data.json', 'r') as file:
        data = json.load(file)
    return data

def load_student_syntax_data(student_id):
    """Returns the syntax categories for a student based on ID in their respective JSON file"""
    with open(f'data/student_data/{student_id}/student_syntax_data.json', 'r') as file:
        data = json.load(file)
    return data

def load_student_card_data(student_id):
    """Returns the relevant card history from relevant student card JSON based on a list of item IDs"""
    with open(f'data/student_data/{student_id}/student_card_data.json', 'r') as file:
        data = json.load(file)
    return data

def normalize_progress(progress):
    """Greek lemmas are progress keys too, so they get the same treatment on load."""
    return {normalize_greek(key): record for key, record in progress.items()}

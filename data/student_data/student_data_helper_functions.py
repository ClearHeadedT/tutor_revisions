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


def normalize_keys(data):
    """Greek appears in item keys, so every key is normalized on load to keep
    the scaffolding and the student's progress joinable"""
    data["items"] = {normalize_greek(key): item for key, item in data["items"].items()}
    return data


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

def student_data_status(student_id):
    student_grammar_data = load_student_grammar_data(student_id)
    student_vocabulary_data = load_student_vocabulary_data(student_id)
    student_syntax_data = load_student_syntax_data(student_id)
    student_card_data = load_student_card_data(student_id)

    return {
        "grammar": normalize_progress(student_grammar_data["grammar"]),
        "vocabulary": normalize_progress(student_vocabulary_data["vocabulary"]),
        "syntax": normalize_progress(student_syntax_data["syntax"]),
        "cards": normalize_progress(student_card_data["cards"])
        }


def normalize_progress(progress):
    return {normalize_greek(key): record for key, record in progress.items()}

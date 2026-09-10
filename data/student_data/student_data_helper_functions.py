import json


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

def load_student_card_data(student_id, id_list):
    """Returns the relevant card history from relevant student card JSON based on a list of item IDs"""
    with open(f'data/student_data/{student_id}/student_card_data.json', 'r') as file:
        data = json.load(file)
    return data

def student_data_status(student_id):
    student_grammar_data = load_student_grammar_data(student_id)
    student_vocabulary_data = load_student_vocabulary_data(student_id)

    return {"grammar": student_grammar_data, "vocabulary": student_vocabulary_data}
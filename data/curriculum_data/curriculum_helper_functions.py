import json

def load_curriculum_json():
    """Returns curriculum in JSON format"""
    with open('data/curriculum_data/full_curriculum.json', 'r') as file:
        data = json.load(file)
    return data

def load_card_randomizer_elements():
    """Returns randomized grammatical elements for card creation"""
    with open('data/curriculum_data/card_randomizer_elements.json', 'r') as file:
        data = json.load(file)
    return data

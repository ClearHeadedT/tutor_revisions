import json
from functools import cache


def load_curriculum_json():
    """Returns curriculum in JSON format"""
    with open('data/curriculum_data/full_curriculum.json', 'r') as file:
        data = json.load(file)
    return data

@cache
def load_scene_bank():
    """The everyday settings a card's sentence may take place in, each tagged with the Louw-Nida
    domains it naturally involves"""
    with open('data/curriculum_data/scene_bank.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def load_vocabulary_items():
    """The vocabulary scaffolding's items, keyed by lemma."""
    with open('data/curriculum_data/vocabulary_scaffolding.json', 'r') as file:
        return json.load(file)["items"]

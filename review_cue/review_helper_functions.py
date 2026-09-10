from datetime import date
from data.student_data.student_data_helper_functions import student_data_status, load_student_card_data


def find_grammar_items_status(student_id):
    student_data = student_data_status(student_id=student_id)
    learned_items = find_learning_recursion("learned", student_data["grammar"])
    learning_items = find_learning_recursion("learning", student_data["grammar"])
    unseen_items = find_learning_recursion("unseen", student_data["grammar"])
    return {
        "learned": learned_items,
        "learning": learning_items,
        "unseen": unseen_items
    }

def find_vocabulary_items_status(student_id):
    student_data = student_data_status(student_id=student_id)
    words = student_data["vocabulary"]["vocabulary"]
    learned_items = {w: internals for w, internals in words.items() if internals["status"] == "learned"}
    learning_items = {w: internals for w, internals in words.items() if internals["status"] == "learning"}
    unseen_items = {w: internals for w, internals in words.items() if internals["status"] == "unseen"}
    return {
        "learned": learned_items,
        "learning": learning_items,
        "unseen": unseen_items
    }

def find_learning_recursion(status, node):
    results = []
    if isinstance(node, dict):
        if node.get("status") == status:
            results.append(node)
        for value in node.values():
            results.extend(find_learning_recursion(status, value))
    return results




def sort_vocabulary_by_due_date(student_id, status="learned"):
    try:
        items_by_status = find_vocabulary_items_status(student_id=student_id)[status]        
    except KeyError:
        print("Valid status options: 'learned' and 'learning'")
        return
    today = date.today()
    day_data_v_reviews = {}
    for word, internals in items_by_status.items():
        word_days_since_review = (today - date.fromisoformat(internals["last_reviewed"])).days
        new_internals = dict(internals)
        new_internals["prior_day_count"] = word_days_since_review
        day_data_v_reviews[word] = new_internals
    return dict(sorted(day_data_v_reviews.items(), key=lambda x: x[1]["prior_day_count"]))

    
def sort_grammar_by_due_date(student_id, status="learned"):
    try:
        items_by_status = find_grammar_items_status(student_id=student_id)[status]        
    except KeyError:
        print("Valid status options: 'learned' and 'learning'")
        return
    today = date.today()
    day_data_g_reviews = {}
    for internals in items_by_status:
        word_days_since_review = (today - date.fromisoformat(internals["last_reviewed"])).days
        new_internals = dict(internals) 
        new_internals["prior_day_count"] = word_days_since_review
        day_data_g_reviews[internals["key"]] = new_internals
    return dict(sorted(day_data_g_reviews.items(), key=lambda x: x[1]["prior_day_count"]))



def card_history_for_items(student_id, due_reviews_list):
    """Returns a dict showing card history for each item of input 'due_reviews_list' keyed by mutual ID"""
    student_card_json = load_student_card_data(student_id=student_id)
    cards_by_id = {}
    for review in due_reviews_list:
        cards_by_id[review["id"]] = student_card_json["id"]["card_history"]
    return cards_by_id



def sort_item_into_difficulty(item):
    




# Some helpful functionality for a "review" day:

# A few lists of review:
#     Basic category
#         Learned only
#         Learning only 
#         Learned and learning 

#     Vocabulary only 
#     Grammar only 
#     Vocabulary and grammar 
    

# What it does basically, two parts:
# (1) REVIEW CREATION PORTION
#     Creates relevant list of reviews for that day 
#     Passes that information on to a card formulator function
#         Card formulator:
#             Tracks history of past card usage 
#             Tracks user level for specific grammar/vocabulary mastery 
#             From that information, sorts relevant items into the correct bucket for either (1) API LLM call or (2) TF text search 
# (2) INTERNAL STATE CHANGER FROM STUDENT FEEDBACK/ANSWERS
    # Basically will change the metadata of the relevant JSON, save card information 
    #     in student_vocabulary_data.JSON Changing student vocabulary item "status" to "learning" 
    #     (assuming there is a 'card' JSON which has saved card occurrences for future reference) save occurrence of card to that JSON and link to item/paradigm by key 
       
         # if previous review was "wrong" then lower difficulty level in JSON 


# Then for the "unseen" items for VOCABULARY:
    # has a default for how many new vocabulary items to add, maybe 5?
    # accesses the relevant known vocabulary pool of the student
    # Accesses the relevant unseen vocabulary pool of the student
    #     (side note - this could be based on their personal goal for books, or just simple GNT frequency occurrence)
    # Utilizes the pre-saved initial card occurrence for however many default items new vocabulary 


# Also need one that increases difficult of card based on time and/or mastery of some sort 

# Think about a combining function that takes multiple vocab/grammar elements into 1 LLM call coherent translation block?

# Student needs progress in grammar tracked 

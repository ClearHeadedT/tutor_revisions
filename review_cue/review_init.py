from .review_helper_functions import sort_vocabulary_by_due_date, card_history_for_items



def vocabulary_review_init(student_id, status="learned", items_limit=None):
    vocabulary_reviews = sort_vocabulary_by_due_date(student_id=student_id, status=status)
    if not items_limit or items_limit > len(vocabulary_reviews):
        items_limit = len(vocabulary_reviews)
    card_history_by_id = card_history_for_items(student_id=student_id, due_reviews_list=vocabulary_reviews)
    for review in vocabulary_reviews:
        card_d_level = review




# I am having to now track the history of each of these items according to their card in JSON by ID to see history 


# have to sort by difficulty level internally. Once 1-4 is accessed from JSON, 
# I can do a simple arg input to relevant card 


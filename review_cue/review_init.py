from .review_helper_functions import sort_vocabulary_by_due_date, card_history_for_items
from data.student_data.student_data_class import StudentVocabulary, StudentGrammar, StudentSyntax





def austin_review():
    """specialized for me working thorugh Gk curriculum,
    implied for me that review cards will be placed further down in process upon initial study"""
    austin_vocabulary_class = StudentVocabulary(student_id="austin")
    austin_grammar_class = StudentGrammar(student_id="austin")
    austin_syntax_class = StudentSyntax(student_id="austin")
    sorted_v_reviews = austin_vocabulary_class.sort_vocabulary_by_due_date()
    sorted_g_reviews = austin_grammar_class.sort_grammar_by_due_date()
    sorted_s_reviews = austin_syntax_class.sort_syntax_by_due_date()


    austin_vocabulary_class.vocabulary_review()


    # for item, internals in sorted_v_reviews.items():
    #     print(item, internals)
    # print("\n")
    # for item, internals in sorted_g_reviews.items():
    #         print(item, internals)
    # print("\n")
    # for item, internals in sorted_s_reviews.items():
    #         print(item, internals)











# def vocabulary_review_init(student_id, status="learned", items_limit=None):
#     vocabulary_reviews = sort_vocabulary_by_due_date(student_id=student_id, status=status)
#     if not items_limit or items_limit > len(vocabulary_reviews):
#         items_limit = len(vocabulary_reviews)
#     # card_history_by_id = card_history_for_items(student_id=student_id, due_reviews_list=vocabulary_reviews)
#     for lemma, internals in vocabulary_reviews.items():
#         pass

#    the goal is to just put the right cards into the right "card" slots
    # is this a single API call or am I really doing like 20? how much more is it each?
    # Probably would be realistic to chunk them idk 


    # for review in vocabulary_reviews.items():
    #     print(review)
    #     print("\n")



# I am having to now track the history of each of these items according to their card in JSON by ID to see history 


# have to sort by difficulty level internally. Once 1-4 is accessed from JSON, 
# I can do a simple arg input to relevant card 


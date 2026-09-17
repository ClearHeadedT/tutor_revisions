# Not yet implemented. Notes carried over from review_cue/ and cards/new_card_class.py
# when those were removed, so the design they recorded survives the restructure.

# What a review session does, in two parts:
# (1) REVIEW CREATION
#     Builds the day's list of reviews from the student's progress
#     Passes it to card formulation:
#         Tracks history of past card usage
#         Tracks user level for specific grammar/vocabulary mastery
#         Sorts items into (1) API LLM call or (2) TF text search
# (2) INTERNAL STATE CHANGE FROM STUDENT FEEDBACK/ANSWERS
#     Writes the result back: item "status", and the card occurrence saved
#     to student_card_data.json linked to the item by key
#         if previous review was "wrong" then lower difficulty level

# Review lists to support:
#     Learned only / learning only / both
#     One domain only, or several together

# For "unseen" vocabulary:
#     A default count of new items to add per session, maybe 5-10
#     Drawn from the unseen pool -- scaffolding keys minus progress keys
#     (could be driven by a personal goal for books, or by GNT frequency)
#     Uses the pre-saved reference card for each new item

# Vocabulary flow already sketched:
#     Cloze first, then text recall as the backup if the cloze is missed
#     Record whether the initial review was correct
#     The reference card serves as the check on comprehension afterward
#     Upon the next review: check card states, sort into the right card type,
#     and make "new" syntax cards for the items answered correctly

# Also needed: something that raises card difficulty based on time and/or mastery
# Consider combining several vocab/grammar items into one LLM call as a coherent
# translation block, rather than one call per card

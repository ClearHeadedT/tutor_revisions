
from data.student_data.student import Student


def sentence_randomizer(student_id, item_grammatical_type, ):




    austin_data = Student(student_id=student_id)
    





# okay, makes sense, a nested dict/JSON that contains the full path to chosen pieces. 
# Four pieces to this broadly, and all will be built from GGBB and syntax summaries in the koine builder directory. That's where a lot of the information I have here has come from.

# The first broad piece is overall syntax/sentence formulation. We have to initially determine what kind of sentence we are utilizing/what structure. As you can trace the logic with what I have here, in the case there's a dependent clause added, there's several options for what that dependent clause could be (broadly), but even more decisions within that broad possibility. I have what I have here, but it's obviously incomplete. You'll need to search the resources and include the primary, common usages of sentence formation, beginning with broad choices and possibilitites and nesting the particulars under those categories. 

# Second piece is specifics of individual items slotted into the sentence structure. These are largely contingent on lexical items the student has learned. 

# Third piece is the actual explanation of each of these syntactic uses, descriptions of what each item/option is, basic rule formulation, etc - ideally derived from the short description sentence or two found in syntax summaries, which explains how the (again - ideally without the biblical references present in the material, but not sure how realistic this will be to parse out without biblical reference, and if there's no overt examples it might not know how to formulate it - so maybe it's best to include them not sure). 

# Fourth piece is being able to access the student history syntax and derive the actual syntactic categories they have studied so that they aren't handed material they are unfamiliar with. How I see this is more of an opening up of new parts of the JSON to include more options dependent on what the student knows/is familiar with. This could get fuzzy potentially, which is why a full curriculum would be helpful here. Once they have a familiarity with the idea syntactically of a causal dependent clause, it could theoretically be displayed, but only once the grammatical, specific uses of an adverbial participle or infinitive are familiarized, too.
# Further, as I'm thinking about this and considering it, I don't think the student will ever learn about "causal clauses" in isolation. It's always going to be attached to the study of an item. They will learn about causal clauses when they are introduced to participles, and then subsequently introduced to a causal adverbial participle in syntax. So there's really only 2 contingencies for unlocking that portion of the JSON. First is the initial study grammatically (grammar item of present act participle masc sng) and second is the syntactic category.
# Thinking even MORE broadly, the individual pieces of the participle itself (from a grammar item morphological standpoint) could then progressively be unlocked as well (present act ind masc singlular, but not yet passive learned, so only 
# I'm guessing this will all happen in the conditionals by key. Keys that are verified as learned by a student in their student object/JSON history will enable the randomized possibility of utilizing these pieces.

# We're only looking for primary uses. That's one reason you will likely see that I don't have EVERY usage/category present for some of the clause options here, just the primary ones that won't be convoluted by an LLM call. 








# The goal: prevent repetitive and biblical text-oriented LLM output 

# Randomizer tool
    # Case by case - vocabulary, syntax, grammar
    # Accesses student object with internal information 
        # New pools of relevant information and possible inclusion 

        # List of common sentence order formulations in the GNT 
        # List of syntactic uses the student has already encountered 
        # List of catered lexical items that can be used alongside of review item in formulation
            # action-oriented verbs
                # Probably those with little inflection
            # prepositions
            # nouns that are covering different concepts and domains to ensure 
            # proper nouns - people, places, things for pairing with other pieces 
        # List of grammar concepts already learned 
            # Especially those of verb tenses, different types of participles, etc 
            # Probably just the primary categories of tenses/uses

        # Implement random selection (probably just using these as a set and it will "draw" a random one)
            # Depending on student level:
                # Beginner:
                    # Always returned:
                        # Simple clause, consistent order
                        # Subject proper noun
                        # Simple form verb
                            # Either simple Aorist, imperfect, or present depending on what student has learned 
                        # Direct object
                    # Random selection inclusion:
                        # Possibility of preposition
                        # Other case possibilities
                            # Semantic emphasis chosen randomly from already-learned genitival syntactic uses, for example 


        # A list of how to form these, along with their morphological information 


# Some considerations of how this could work to make it coherent and consistent 

# The "object" list, or even the subject, prepositions, and more, could be linked together by the primary verb. 
    # Verb carries the force semantically, so the pieces fit under the umbrella of verb 
# Similarly, many forms are often semantically and grammatically tied, like genitives, datives, participles, adverbs, etc
    # They can't just be thrown together in a non-coherent fashion
    # But it also doesn't have to be over-engineered to the point of every piece perfectly fitting together




# List of variables to be chosen from:
    # Primary verb:
        # Voice variation - active, middle, passive 
        # Mood variation - indicative, subjunctive, imperative 
        # Tense variation - present, imperfect, aorist, future, perfect 
    # Secondary/supplementary verbal:
        # Infinitive
            # Voice either active or middle/passive 
            # Tense present or aorist 
            # Adverbial or substantival 
        # Participle
            # Present, aorist, perfect tense 
            # Active and passive 
            # Adjectival/substantival participle 
            # Verbal participles
    # Subject nominal:
        # Simple subject, connected to verb
    # Object nominal:
        # Direct object (assuming it's required by the verbal)
    # Supplementary nominals:
        # Genitive, dative
    # Particles/connectors
        # Logical conjunctions list
        # Adverbial conjunctions
        # Substantival conjunctions
        # Conditionals
        # Negators/prohibitions
        # Prepositions
            # Will need attached list of coherent complements and required substantive case

    # Broad categories of dependent clause construction "type" possibilities (note - related to particles):
        # infinitival clause
        # participial clause
        # conjunctive clause
        # relative clause

    # Broad categories of syntactic dependent clause usage:
        # Subject
            # Substantival infinitive, participle, ὅτι + indicative mood, ἵνα + subjunctive, relative pronoun
        # Direct object (same specifics as subject above)





















# Okay, I'm hoping to utilize the search functionality in this project for a specific task. Use hybrid search for this and tweak the parameters however you find helpful and necessary. 
# Basically I'm building functionality to randomly select elements of grammar to make a unique sentence composed of the pieces. For this, I need all the grammar pieces in reasonable layout for selection. 

# This is what I have so far: 

# List of variables to be chosen from:
    # Primary verb:
        # Voice variation - active, middle, passive 
        # Mood variation - indicative, subjunctive, imperative 
        # Tense variation - present, imperfect, aorist, future, perfect 
    # Secondary/supplementary verbal:
        # Infinitive
            # Voice either active or middle/passive 
            # Tense present or aorist 
            # Adverbial or substantival 
        # Participle
            # Present, aorist, perfect tense 
            # Active and passive 
            # Adjectival/substantival participle 
            # Verbal participles
    # Subject nominal:
        # Simple subject, connected to verb
    # Object nominal:
        # Direct object (assuming it's required by the verbal)
    # Supplementary nominals:
        # Genitive, dative
    # Particles/connectors
        # Logical conjunctions list
        # Adverbial conjunctions
        # Substantival conjunctions
        # Conditionals
        # Negators/prohibitions
        # Prepositions
            # Will need attached list of coherent complements and required substantive case

    # Broad categories of dependent clause construction "type" possibilities (note - related to particles):
        # infinitival clause
        # participial clause
        # conjunctive clause
        # relative clause


# Notice this is predominately thinking of broad function here, not focusing on individual syntactic use, but the individual syntactic possibilities in something like syntax_summaries or GGBB will be implemented, too, on a basis of student familiarity 
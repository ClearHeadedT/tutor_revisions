
from data.student_data.student import Student


def sentence_randomizer(student_id="austin"):
    broad_sentence_form = {"simple_beginner", "main_with_dependent", "two_completes_coordinating"}

    dependent_clause_possibilities_broad = {"substantival", "adverbial"}
    substantival_clause_possibilities_broad = {"subject", "direct_object"}
    adverbial_clause_possibilities_broad = {"causal", "concessive", "conditional", "manner_means", "purpose", "resultative", "time"}
    causal_clause_possibilites_items = {"infinitive", "adverbial_participle", "oti_indicative"}
    concessive_clause_possibilites_items = {"adverbial_participle", "ei_kai_indicative"}
    conditional_clause_possibilites_items = {"first_class", "second_class", "third_class"}
    manner_means_clause_possibilites_items = {"articular_infinitive", "adverbial_participle", "relative_pn_hon"}
    purpose_clause_possibilites_items = {"infinitive", "adverbial_participle", "hina_subjunctive", "relative_pn_hoitines"}
    resultative_clause_possibilities_items = {"infinitive", "adverbial_participle", "hina_subjunctive", "relative_adverb_hothen"}
    time_clause_possibilites_items = {"articular_infinitive", "adverbial_participle", "hote_indicative", "relative_pn"}

    infinitive_morphological_possibilites = {""}

    austin_data = Student(student_id=student_id)
    







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
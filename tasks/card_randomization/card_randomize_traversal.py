

# default_position / marked_position sit on the semantic clause type, not on its realization:
# a conditional participle precedes and a result participle follows, exactly as the matching
# conjunction would. Rationale and sources in grammatical_instructions.py.


traversal = {
    "word_order": {
        "unmarked_clause_order": ["subject", "predicate", "complement"],
        "unmarked_clause_order_notes": {
            "predicate_is_minimal": "A Greek clause may consist of the predicate alone.",
            "complement_is_mobile": "Either side of the predicate, slightly favouring after.",
            "subject_first_is_meaningful": "Marks the topic or a shift of topic; the force "
                                           "weakens as the subject moves right.",
            "imperative_exception": "In clauses with an imperative the predicate is fronted.",
        },
        "unmarked_deviations": [
            "pronoun subject moves before the verb",
            "pronoun object sits immediately after the verb (direct before indirect)",
            "a clause-shaped subject or object moves to the rear of the main clause",
            "a negative stands immediately before the verb",
        ],
        "fronting_triggers": {
            "contrast": "front BOTH contrasted elements, each before its own verb",
            "contraexpectation": "front the element that defeats the expectation",
            "comparison": "front both compared elements, each before its own verb",
            "topicalization": "front a newly introduced topic",
            "motif": "front the first mention of a recurring motif; often accusative",
            "rhetorical": "front the element carrying the speaker's emotion or expectation",
        },
        "hard_constraints": {
            "article_precedes_substantive": "ὁ θεός, never θεὸς ὁ",
            "preposition_precedes_object": "exceptions χάριν, χωρίς, ἕνεκα are rare",
            "relative_and_interrogative_are_clause_initial":
                "whatever their grammatical function inside the clause",
            "postpositive_never_opens_a_clause": {
                "words": ["ἄν", "γάρ", "δέ", "γέ", "μέν", "οὖν",
                          "ποτέ", "πώς", "τέ", "με", "μου", "μοι"],
                "slot": "anywhere from directly after the first word to just past the first "
                        "complete phrase - a range, not a fixed second position",
            },
            "never_closes_a_clause": ["ἀλλά", "ἤ", "καί", "οὐδέ", "μηδέ", "οὔτε", "μήτε",
                                      "εἴτε", "μή", "εἰ", "ἐπεί", "ἵνα", "ὁ",
                                      "relative pronouns", "most prepositions"],
            "tends_to_the_front": ["interrogatives", "clause negatives", "πρῶτον", "ἔπειτα",
                                   "εἶτα", "nominative demonstratives", "νῦν", "τότε", "αὐτός",
                                   "ἄλλος", "ἕτερος", "ἀμφότεροι", "πολύς", "πολλάκις", "εἷς"],
            "negative_scope": "A negative immediately before the verb negates the whole clause; "
                              "before any other element it negates only that element.",
        },
        "phrase_internal_tendencies": {
            "genitive_modifier": "follows its noun - 96% Paul, 99% Luke",
            "demonstrative": "follows its noun - 85% Paul, 78% Luke",
            "adjective": "follows its noun ~75% in Luke and Mark, but PRECEDES ~65% in Paul",
            "stacked_modifier_order": ["head noun", "demonstrative", "indefinite",
                                       "numeral", "descriptive", "participle"],
            "adverb_phrase": "rarely comes between a verb and its object; put it on one side",
        },
    },

    "sentence_construction_possibilitites": {
        "simple_beginner_sentence": {},
        "main_and_dependent_sentence": {
            "adverbial": {
                "causal": {
                    "position": {"default": "after", "marked": "before"},
                    "usages": {
                        "infinitive": {},
                        "adverbial_participle": {},
                        "oti_indicative": {}
                    }
                },
                "concessive": {
                    "position": {"default": "after", "marked": "before"},
                    "usages": {
                        "adverbial_participle": {},
                        "ei_kai_indicative": {}
                    }
                },
                "conditional": {
                    "position": {"default": "before", "marked": "after"},
                    "usages": {
                        "first_class": {},
                        "second_class": {},
                        "third_class": {}
                    }
                },
                "manner_means": {
                    "position": {"default": "after", "marked": "before"},
                    "usages": {
                        "articular_infinitive": {},
                        "adverbial_participle": {},
                        "relative_pn_hon": {}
                    }
                },
                "purpose": {
                    "position": {"default": "after", "marked": "before"},
                    "usages": {
                        "infinitive": {},
                        "adverbial_participle": {},
                        "hina_subjunctive": {},
                        "relative_pn_hoitines": {}
                    }
                },
                "resultative": {
                    "position": {"default": "after", "marked": "before"},
                    "usages": {
                        "infinitive": {},
                        "adverbial_participle": {},
                        "hina_subjunctive": {},
                        "relative_adverb_hothen": {}
                    }
                },
                "time": {
                    "position": {"default": "split", "marked": "split"},
                    "usages": {
                        "articular_infinitive": {},
                        "adverbial_participle": {},
                        "hote_indicative": {},
                        "relative_pn": {}
                    }
                },
                "comparative": {
                    "position": {"default": "after", "marked": "before"},
                    "usages": {
                        "adverbial_participle": {},
                        "kathos_hos_indicative": {}
                    }
                },
                "local": {
                    "position": {"default": "after", "marked": "before"},
                    "usages": {
                        "hopou_indicative": {},
                        "relative_adverb_hou": {}
                    }
                }
            }
        },
        "main_and_relative_sentence": {
            "position": {"default": "after", "marked": "before"},
            "substantival": {
                "indicative": {
                    "usages": {
                        "subject": {},
                        "object": {},
                        "independent": {}
                    }
                },
                "subjunctive": {}
            },
            "adjectival": {}
        },
        "two_complete_coordinating_sentence": {
            "connector_piece": {}
        }
    },
    "sentence_vitals": {
        "verb": {
            "usages": {
                "finite_verb": {},
                "finite_with_infinitive_complement": {}
            }
        },
        "subject": {
            "usages": {
                "nominative": {},
                "substantival_participle": {},
                "hoti_indicative": {},
                "hina_subjunctive": {},
                "relative_pn_ho": {}
            }
        },
        "object": {
            "usages": {
                "accusative": {},
                "substantival_participle": {},
                "relative_clause": {},
                "substantival_infinitive": {},
                "hoti_indicative": {},
                "hina_subjunctive": {}
            }
        }
    },
    "other_supplementary_pieces": {
        "extra_case_usage": {
            "usages": {
                "genitive": {},
                "dative": {}
            }
        },
        "adverbial": {
            "usages": {
                "verbal_modification_proper": {},
                "substantival_modification": {}
            }
        },
       "prepositions": {},
       "particles": {}
    }
}




# Keep the "item" portions empty -
# ready to fill in as possibilites in sep function based on student data and choice selection
    # grammar items individual forms AND syntax?

# As for categories like "particles", whatever is present in the other categories as makeup should be excluded
# so there isn't incoherent logic within the sentence

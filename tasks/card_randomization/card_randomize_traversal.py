import json
from pathlib import Path

# default_position / marked_position sit on the semantic clause type, not on its realization:
# a conditional participle precedes and a result participle follows, exactly as the matching
# conjunction would. Rationale and sources in grammatical_instructions.py.
#
# Usages are written empty here and filled by _wire() at the bottom of the file. The two keys
# that gate a usage - the syntactic category and the grammatical forms it is built from - live
# in traversal_wiring.json, built by derivation/wire_traversal.py. Keeping them out of this file
# keeps the shape readable: the wiring runs to a median of seventeen grammar keys per usage.


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


# Usages are keyed here exactly as formation_instructions keys them, so one path reaches the
# instructions, the wiring and the traversal node alike. The only difference is that the
# traversal nests its options under "usages", which _walk steps over.
WIRING_PATH = Path("data/curriculum_data/traversal_wiring.json")


def _walk(path):
    """The traversal node at a dotted formation-instructions path, or None.

    Every step tries the plain key first and then the same key under "usages", which is where
    the traversal keeps a node's options."""
    node = traversal
    for step in path.split("."):
        if not isinstance(node, dict):
            return None
        if step in node:
            node = node[step]
        elif "usages" in node and step in node["usages"]:
            node = node["usages"][step]
        else:
            return None
    return node


def _wire():
    """Fill each usage with its syntactic_item and grammatical_items.

    A usage with neither is unavailable to every student, which is how the empty placeholders
    read before this ran - and why the randomizer raised on its first call."""
    if not WIRING_PATH.exists():
        return 0
    wiring = json.loads(WIRING_PATH.read_text(encoding="utf-8"))
    filled = 0
    for path, keys in wiring.items():
        node = _walk(path)
        if node is None:
            continue
        node.update(keys)
        filled += 1
    return filled


WIRED_USAGES = _wire()

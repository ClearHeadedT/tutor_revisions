# Plan run preview

No API calls. Each item's user message as generation would send it; the system prompt is the card type's instructions and is the same for every item of a category.

## grammar — `text_recall_grammar_g2e`

### `article::ὁ::nominative.masculine.singular`

```json
{
  "item": {
    "item": {
      "key": "article::ὁ::nominative.masculine.singular",
      "parent": "article::ὁ",
      "rule": "article",
      "form": "ὁ",
      "parsing": "nominative masculine singular",
      "features": {
        "case": "nominative",
        "gender": "masculine",
        "number": "singular"
      },
      "lexical_form": "ὁ"
    },
    "rule": {
      "name": "Definite Article",
      "sequence": 81,
      "pos_lex_category": "noun",
      "morph_rule_description": "Twenty-four forms carrying first and second declension case endings across all three genders. It is the smallest complete display of the case-ending system, and the most frequent word in the corpus.",
      "paradigms": {
        "article::ὁ": {
          "type": "noun",
          "lexical_form": "ὁ",
          "source": [
            {
              "resource": "GrammarSummaries",
              "chapter": "Appendix",
              "header": "Definite Article",
              "page": null
            }
          ],
          "slots": [
            "article::ὁ::nominative.masculine.singular",
            "article::ὁ::genitive.masculine.singular",
            "article::ὁ::dative.masculine.singular",
            "article::ὁ::accusative.masculine.singular",
            "article::ὁ::nominative.masculine.plural",
            "article::ὁ::genitive.masculine.plural",
            "article::ὁ::dative.masculine.plural",
            "article::ὁ::accusative.masculine.plural"
          ],
          "gnt_lemma_frequency": 19783
        },
        "article::ἡ": {
          "type": "noun",
          "lexical_form": "ἡ",
          "source": [
            {
              "resource": "GrammarSummaries",
              "chapter": "Appendix",
              "header": "Definite Article",
              "page": null
            }
          ],
          "slots": [
            "article::ἡ::nominative.feminine.singular",
            "article::ἡ::genitive.feminine.singular",
            "article::ἡ::dative.feminine.singular",
            "article::ἡ::accusative.feminine.singular",
            "article::ἡ::nominative.feminine.plural",
            "article::ἡ::genitive.feminine.plural",
            "article::ἡ::dative.feminine.plural",
            "article::ἡ::accusative.feminine.plural"
          ]
        },
        "article::τό": {
          "type": "noun",
          "lexical_form": "τό",
          "source": [
            {
              "resource": "GrammarSummaries",
              "chapter": "Appendix",
              "header": "Definite Article",
              "page": null
            }
          ],
          "slots": [
            "article::τό::nominative.neuter.singular",
            "article::τό::genitive.neuter.singular",
            "article::τό::dative.neuter.singular",
            "article::τό::accusative.neuter.singular",
            "article::τό::nominative.neuter.plural",
            "article::τό::genitive.neuter.plural",
            "article::τό::dative.neuter.plural",
            "article::τό::accusative.neuter.plural"
          ]
        }
      },
      "difficulty_tier": 1,
      "teaching_note": "No other word inflects like the article, so drill_lexemes is empty by nature rather than by omission. GrammarSummaries' Eight Noun Rules 2, 3 and 6 are all visible in this one chart: neuter nominative and accusative match, neuter plural ends in alpha, and masculine and neuter are identical in the genitive and dative.",
      "drill_lexemes": []
    },
    "paradigm": {
      "type": "noun",
      "lexical_form": "ὁ",
      "source": [
        {
          "resource": "GrammarSummaries",
          "chapter": "Appendix",
          "header": "Definite Article",
          "page": null
        }
      ],
      "slots": [
        "article::ὁ::nominative.masculine.singular",
        "article::ὁ::genitive.masculine.singular",
        "article::ὁ::dative.masculine.singular",
        "article::ὁ::accusative.masculine.singular",
        "article::ὁ::nominative.masculine.plural",
        "article::ὁ::genitive.masculine.plural",
        "article::ὁ::dative.masculine.plural",
        "article::ὁ::accusative.masculine.plural"
      ],
      "gnt_lemma_frequency": 19783
    }
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a single main clause",
      "formation": "A single independent clause: nominative subject, finite verb, and an accusative direct object if the verb is transitive.",
      "function": "One unsubordinated assertion. Unmarked order is subject, then predicate, then complement."
    },
    "also_include": [],
    "setting_options": {
      "s124": "A young man is made treasurer of a trade guild and the older members doubt him.",
      "s013": "An old teacher tests his pupils on the letters they copied onto wax tablets."
    }
  }
}
```

### `article::ἡ::genitive.feminine.singular`

```json
{
  "item": {
    "item": {
      "key": "article::ἡ::genitive.feminine.singular",
      "parent": "article::ἡ",
      "rule": "article",
      "form": "τῆς",
      "parsing": "genitive feminine singular",
      "features": {
        "case": "genitive",
        "gender": "feminine",
        "number": "singular"
      },
      "lexical_form": "ἡ"
    },
    "rule": {
      "name": "Definite Article",
      "sequence": 81,
      "pos_lex_category": "noun",
      "morph_rule_description": "Twenty-four forms carrying first and second declension case endings across all three genders. It is the smallest complete display of the case-ending system, and the most frequent word in the corpus.",
      "paradigms": {
        "article::ὁ": {
          "type": "noun",
          "lexical_form": "ὁ",
          "source": [
            {
              "resource": "GrammarSummaries",
              "chapter": "Appendix",
              "header": "Definite Article",
              "page": null
            }
          ],
          "slots": [
            "article::ὁ::nominative.masculine.singular",
            "article::ὁ::genitive.masculine.singular",
            "article::ὁ::dative.masculine.singular",
            "article::ὁ::accusative.masculine.singular",
            "article::ὁ::nominative.masculine.plural",
            "article::ὁ::genitive.masculine.plural",
            "article::ὁ::dative.masculine.plural",
            "article::ὁ::accusative.masculine.plural"
          ],
          "gnt_lemma_frequency": 19783
        },
        "article::ἡ": {
          "type": "noun",
          "lexical_form": "ἡ",
          "source": [
            {
              "resource": "GrammarSummaries",
              "chapter": "Appendix",
              "header": "Definite Article",
              "page": null
            }
          ],
          "slots": [
            "article::ἡ::nominative.feminine.singular",
            "article::ἡ::genitive.feminine.singular",
            "article::ἡ::dative.feminine.singular",
            "article::ἡ::accusative.feminine.singular",
            "article::ἡ::nominative.feminine.plural",
            "article::ἡ::genitive.feminine.plural",
            "article::ἡ::dative.feminine.plural",
            "article::ἡ::accusative.feminine.plural"
          ]
        },
        "article::τό": {
          "type": "noun",
          "lexical_form": "τό",
          "source": [
            {
              "resource": "GrammarSummaries",
              "chapter": "Appendix",
              "header": "Definite Article",
              "page": null
            }
          ],
          "slots": [
            "article::τό::nominative.neuter.singular",
            "article::τό::genitive.neuter.singular",
            "article::τό::dative.neuter.singular",
            "article::τό::accusative.neuter.singular",
            "article::τό::nominative.neuter.plural",
            "article::τό::genitive.neuter.plural",
            "article::τό::dative.neuter.plural",
            "article::τό::accusative.neuter.plural"
          ]
        }
      },
      "difficulty_tier": 1,
      "teaching_note": "No other word inflects like the article, so drill_lexemes is empty by nature rather than by omission. GrammarSummaries' Eight Noun Rules 2, 3 and 6 are all visible in this one chart: neuter nominative and accusative match, neuter plural ends in alpha, and masculine and neuter are identical in the genitive and dative.",
      "drill_lexemes": []
    },
    "paradigm": {
      "type": "noun",
      "lexical_form": "ἡ",
      "source": [
        {
          "resource": "GrammarSummaries",
          "chapter": "Appendix",
          "header": "Definite Article",
          "page": null
        }
      ],
      "slots": [
        "article::ἡ::nominative.feminine.singular",
        "article::ἡ::genitive.feminine.singular",
        "article::ἡ::dative.feminine.singular",
        "article::ἡ::accusative.feminine.singular",
        "article::ἡ::nominative.feminine.plural",
        "article::ἡ::genitive.feminine.plural",
        "article::ἡ::dative.feminine.plural",
        "article::ἡ::accusative.feminine.plural"
      ]
    }
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "two independent clauses joined by a coordinating conjunction",
      "formation": "A coordinating conjunction between two independent clauses. Connective: καί, δέ. Contrastive: ἀλλά, δέ, πλήν. Correlative: μέν … δέ, καί … καί. Inferential: οὖν, ἄρα, διό. Explanatory: γάρ. Disjunctive: ἤ.",
      "function": "Carries the movement of thought from one clause to the next by naming the logical relation between them. Both clauses stay independent.",
      "note": "γάρ, δέ, οὖν and μέν are postpositive and cannot stand first in their clause. See the hard constraints under WORD ORDER.",
      "syntactic_category": "Connective (continuative, coordinate) - a syntactic usage, under Conjunctions. Syntactic explanation: and, also (if emphatic [adjunctive]); (connects an additional element to a discussion); καί and δέ."
    },
    "also_include": [],
    "setting_options": {
      "s047": "Two old friends meet after years apart at the city baths.",
      "s112": "A servant carries a lamp ahead of his master along a dark street."
    }
  }
}
```

### `article::τό::dative.neuter.plural`

```json
{
  "item": {
    "item": {
      "key": "article::τό::dative.neuter.plural",
      "parent": "article::τό",
      "rule": "article",
      "form": "τοῖς",
      "parsing": "dative neuter plural",
      "features": {
        "case": "dative",
        "gender": "neuter",
        "number": "plural"
      },
      "lexical_form": "τό"
    },
    "rule": {
      "name": "Definite Article",
      "sequence": 81,
      "pos_lex_category": "noun",
      "morph_rule_description": "Twenty-four forms carrying first and second declension case endings across all three genders. It is the smallest complete display of the case-ending system, and the most frequent word in the corpus.",
      "paradigms": {
        "article::ὁ": {
          "type": "noun",
          "lexical_form": "ὁ",
          "source": [
            {
              "resource": "GrammarSummaries",
              "chapter": "Appendix",
              "header": "Definite Article",
              "page": null
            }
          ],
          "slots": [
            "article::ὁ::nominative.masculine.singular",
            "article::ὁ::genitive.masculine.singular",
            "article::ὁ::dative.masculine.singular",
            "article::ὁ::accusative.masculine.singular",
            "article::ὁ::nominative.masculine.plural",
            "article::ὁ::genitive.masculine.plural",
            "article::ὁ::dative.masculine.plural",
            "article::ὁ::accusative.masculine.plural"
          ],
          "gnt_lemma_frequency": 19783
        },
        "article::ἡ": {
          "type": "noun",
          "lexical_form": "ἡ",
          "source": [
            {
              "resource": "GrammarSummaries",
              "chapter": "Appendix",
              "header": "Definite Article",
              "page": null
            }
          ],
          "slots": [
            "article::ἡ::nominative.feminine.singular",
            "article::ἡ::genitive.feminine.singular",
            "article::ἡ::dative.feminine.singular",
            "article::ἡ::accusative.feminine.singular",
            "article::ἡ::nominative.feminine.plural",
            "article::ἡ::genitive.feminine.plural",
            "article::ἡ::dative.feminine.plural",
            "article::ἡ::accusative.feminine.plural"
          ]
        },
        "article::τό": {
          "type": "noun",
          "lexical_form": "τό",
          "source": [
            {
              "resource": "GrammarSummaries",
              "chapter": "Appendix",
              "header": "Definite Article",
              "page": null
            }
          ],
          "slots": [
            "article::τό::nominative.neuter.singular",
            "article::τό::genitive.neuter.singular",
            "article::τό::dative.neuter.singular",
            "article::τό::accusative.neuter.singular",
            "article::τό::nominative.neuter.plural",
            "article::τό::genitive.neuter.plural",
            "article::τό::dative.neuter.plural",
            "article::τό::accusative.neuter.plural"
          ]
        }
      },
      "difficulty_tier": 1,
      "teaching_note": "No other word inflects like the article, so drill_lexemes is empty by nature rather than by omission. GrammarSummaries' Eight Noun Rules 2, 3 and 6 are all visible in this one chart: neuter nominative and accusative match, neuter plural ends in alpha, and masculine and neuter are identical in the genitive and dative.",
      "drill_lexemes": []
    },
    "paradigm": {
      "type": "noun",
      "lexical_form": "τό",
      "source": [
        {
          "resource": "GrammarSummaries",
          "chapter": "Appendix",
          "header": "Definite Article",
          "page": null
        }
      ],
      "slots": [
        "article::τό::nominative.neuter.singular",
        "article::τό::genitive.neuter.singular",
        "article::τό::dative.neuter.singular",
        "article::τό::accusative.neuter.singular",
        "article::τό::nominative.neuter.plural",
        "article::τό::genitive.neuter.plural",
        "article::τό::dative.neuter.plural",
        "article::τό::accusative.neuter.plural"
      ]
    }
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "two independent clauses joined by a coordinating conjunction",
      "formation": "A coordinating conjunction between two independent clauses. Connective: καί, δέ. Contrastive: ἀλλά, δέ, πλήν. Correlative: μέν … δέ, καί … καί. Inferential: οὖν, ἄρα, διό. Explanatory: γάρ. Disjunctive: ἤ.",
      "function": "Carries the movement of thought from one clause to the next by naming the logical relation between them. Both clauses stay independent.",
      "note": "γάρ, δέ, οὖν and μέν are postpositive and cannot stand first in their clause. See the hard constraints under WORD ORDER.",
      "syntactic_category": "Connective (continuative, coordinate) - a syntactic usage, under Conjunctions. Syntactic explanation: and, also (if emphatic [adjunctive]); (connects an additional element to a discussion); καί and δέ."
    },
    "also_include": [],
    "setting_options": {
      "s067": "A traveller's sandal strap breaks on a mountain road far from the next town.",
      "s154": "A pair of oxen cannot pull the cart out of the mud."
    }
  }
}
```

### `article::ἡ::accusative.feminine.plural`

```json
{
  "item": {
    "item": {
      "key": "article::ἡ::accusative.feminine.plural",
      "parent": "article::ἡ",
      "rule": "article",
      "form": "τάς",
      "parsing": "accusative feminine plural",
      "features": {
        "case": "accusative",
        "gender": "feminine",
        "number": "plural"
      },
      "lexical_form": "ἡ"
    },
    "rule": {
      "name": "Definite Article",
      "sequence": 81,
      "pos_lex_category": "noun",
      "morph_rule_description": "Twenty-four forms carrying first and second declension case endings across all three genders. It is the smallest complete display of the case-ending system, and the most frequent word in the corpus.",
      "paradigms": {
        "article::ὁ": {
          "type": "noun",
          "lexical_form": "ὁ",
          "source": [
            {
              "resource": "GrammarSummaries",
              "chapter": "Appendix",
              "header": "Definite Article",
              "page": null
            }
          ],
          "slots": [
            "article::ὁ::nominative.masculine.singular",
            "article::ὁ::genitive.masculine.singular",
            "article::ὁ::dative.masculine.singular",
            "article::ὁ::accusative.masculine.singular",
            "article::ὁ::nominative.masculine.plural",
            "article::ὁ::genitive.masculine.plural",
            "article::ὁ::dative.masculine.plural",
            "article::ὁ::accusative.masculine.plural"
          ],
          "gnt_lemma_frequency": 19783
        },
        "article::ἡ": {
          "type": "noun",
          "lexical_form": "ἡ",
          "source": [
            {
              "resource": "GrammarSummaries",
              "chapter": "Appendix",
              "header": "Definite Article",
              "page": null
            }
          ],
          "slots": [
            "article::ἡ::nominative.feminine.singular",
            "article::ἡ::genitive.feminine.singular",
            "article::ἡ::dative.feminine.singular",
            "article::ἡ::accusative.feminine.singular",
            "article::ἡ::nominative.feminine.plural",
            "article::ἡ::genitive.feminine.plural",
            "article::ἡ::dative.feminine.plural",
            "article::ἡ::accusative.feminine.plural"
          ]
        },
        "article::τό": {
          "type": "noun",
          "lexical_form": "τό",
          "source": [
            {
              "resource": "GrammarSummaries",
              "chapter": "Appendix",
              "header": "Definite Article",
              "page": null
            }
          ],
          "slots": [
            "article::τό::nominative.neuter.singular",
            "article::τό::genitive.neuter.singular",
            "article::τό::dative.neuter.singular",
            "article::τό::accusative.neuter.singular",
            "article::τό::nominative.neuter.plural",
            "article::τό::genitive.neuter.plural",
            "article::τό::dative.neuter.plural",
            "article::τό::accusative.neuter.plural"
          ]
        }
      },
      "difficulty_tier": 1,
      "teaching_note": "No other word inflects like the article, so drill_lexemes is empty by nature rather than by omission. GrammarSummaries' Eight Noun Rules 2, 3 and 6 are all visible in this one chart: neuter nominative and accusative match, neuter plural ends in alpha, and masculine and neuter are identical in the genitive and dative.",
      "drill_lexemes": []
    },
    "paradigm": {
      "type": "noun",
      "lexical_form": "ἡ",
      "source": [
        {
          "resource": "GrammarSummaries",
          "chapter": "Appendix",
          "header": "Definite Article",
          "page": null
        }
      ],
      "slots": [
        "article::ἡ::nominative.feminine.singular",
        "article::ἡ::genitive.feminine.singular",
        "article::ἡ::dative.feminine.singular",
        "article::ἡ::accusative.feminine.singular",
        "article::ἡ::nominative.feminine.plural",
        "article::ἡ::genitive.feminine.plural",
        "article::ἡ::dative.feminine.plural",
        "article::ἡ::accusative.feminine.plural"
      ]
    }
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with an adverbial dependent clause: causal, adverbial participle",
      "formation": "Anarthrous participle matching its subject in case, number and gender. It usually sits ahead of the verb it modifies.",
      "function": "Supplies the ground or reason for the finite verb - it answers 'Why?'. Render with 'because'.",
      "syntactic_category": "Cause - a syntactic usage, under Participle > Verbal Participles > Dependent Verbal Participles > Adverbial (or Circumstantial). Syntactic explanation: because (answers the question, Why?); indicates the cause or reason or ground of the action of the finite verb; usually precedes its verb.",
      "position": "after the main clause by default; before it when you mean to give it emphasis",
      "paradigm": {
        "name": "First Aorist Active Participle",
        "forms": {
          "λύσας (λύω, thematic)": {
            "aorist active participle nominative masculine singular": "λύσας",
            "aorist active participle genitive masculine singular": "λύσαντος",
            "aorist active participle dative masculine singular": "λύσαντι",
            "aorist active participle accusative masculine singular": "λύσαντα",
            "aorist active participle nominative masculine plural": "λύσαντες",
            "aorist active participle genitive masculine plural": "λυσάντων",
            "aorist active participle dative masculine plural": "λύσασι(ν)",
            "aorist active participle accusative masculine plural": "λύσαντας"
          },
          "λύσασα (λύω, thematic)": {
            "aorist active participle nominative feminine singular": "λύσασα",
            "aorist active participle genitive feminine singular": "λυσάσης",
            "aorist active participle dative feminine singular": "λυσάσῃ",
            "aorist active participle accusative feminine singular": "λύσασαν",
            "aorist active participle nominative feminine plural": "λύσασαι",
            "aorist active participle genitive feminine plural": "λυσασῶν",
            "aorist active participle dative feminine plural": "λυσάσαις",
            "aorist active participle accusative feminine plural": "λυσάσας"
          },
          "λῦσαν (λύω, thematic)": {
            "aorist active participle nominative neuter singular": "λῦσαν",
            "aorist active participle genitive neuter singular": "λύσαντος",
            "aorist active participle dative neuter singular": "λύσαντι",
            "aorist active participle accusative neuter singular": "λῦσαν",
            "aorist active participle nominative neuter plural": "λύσαντα",
            "aorist active participle genitive neuter plural": "λυσάντων",
            "aorist active participle dative neuter plural": "λύσασι(ν)",
            "aorist active participle accusative neuter plural": "λύσαντα"
          },
          "στήσας (ἵστημι, first aorist)": {
            "aorist active participle nominative masculine singular": "στήσας",
            "aorist active participle genitive masculine singular": "στήσαντος"
          },
          "στήσασα (ἵστημι, first aorist)": {
            "aorist active participle nominative feminine singular": "στήσασα",
            "aorist active participle genitive feminine singular": "στησάσης"
          },
          "στήσαν (ἵστημι, first aorist)": {
            "aorist active participle nominative neuter singular": "στήσαν",
            "aorist active participle genitive neuter singular": "στήσαντος"
          },
          "θήκας (τίθημι, κ-aorist)": {
            "aorist active participle nominative masculine singular": "θήκας",
            "aorist active participle genitive masculine singular": "θήκαντος"
          },
          "θήκασα (τίθημι, κ-aorist)": {
            "aorist active participle nominative feminine singular": "θήκασα",
            "aorist active participle genitive feminine singular": "θηκάσης"
          },
          "θήκαν (τίθημι, κ-aorist)": {
            "aorist active participle nominative neuter singular": "θήκαν",
            "aorist active participle genitive neuter singular": "θήκαντος"
          }
        }
      }
    },
    "also_include": [],
    "setting_options": {
      "s114": "A tanner is shunned by his neighbours for the smell of his trade.",
      "s019": "A girl hides her brother's broken toy from their father."
    }
  }
}
```

### `decl2::λόγος::nominative.singular`

```json
{
  "item": {
    "item": {
      "key": "decl2::λόγος::nominative.singular",
      "parent": "decl2::λόγος",
      "rule": "decl2",
      "form": "λόγος",
      "parsing": "nominative singular",
      "features": {
        "case": "nominative",
        "number": "singular"
      },
      "lexical_form": "λόγος"
    },
    "rule": {
      "name": "Second Declension Nouns",
      "sequence": 9,
      "pos_lex_category": "noun",
      "morph_rule_description": "Stems ending in omicron. Masculine nouns take -ος in the nominative singular, neuter nouns -ον, and the two differ only in the nominative and accusative.",
      "paradigms": {
        "decl2::λόγος": {
          "type": "noun",
          "lexical_form": "λόγος",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::λόγος::nominative.singular",
            "decl2::λόγος::genitive.singular",
            "decl2::λόγος::dative.singular",
            "decl2::λόγος::accusative.singular",
            "decl2::λόγος::vocative.singular",
            "decl2::λόγος::nominative.plural",
            "decl2::λόγος::genitive.plural",
            "decl2::λόγος::dative.plural",
            "decl2::λόγος::accusative.plural"
          ],
          "gnt_lemma_frequency": 331
        },
        "decl2::ὁδός": {
          "type": "noun",
          "lexical_form": "ὁδός",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::ὁδός::nominative.singular",
            "decl2::ὁδός::genitive.singular",
            "decl2::ὁδός::dative.singular",
            "decl2::ὁδός::accusative.singular",
            "decl2::ὁδός::vocative.singular",
            "decl2::ὁδός::nominative.plural",
            "decl2::ὁδός::genitive.plural",
            "decl2::ὁδός::dative.plural",
            "decl2::ὁδός::accusative.plural"
          ],
          "gnt_lemma_frequency": 101
        },
        "decl2::ἔργον": {
          "type": "noun",
          "lexical_form": "ἔργον",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::ἔργον::nominative.singular",
            "decl2::ἔργον::genitive.singular",
            "decl2::ἔργον::dative.singular",
            "decl2::ἔργον::accusative.singular",
            "decl2::ἔργον::vocative.singular",
            "decl2::ἔργον::nominative.plural",
            "decl2::ἔργον::genitive.plural",
            "decl2::ἔργον::dative.plural",
            "decl2::ἔργον::accusative.plural"
          ],
          "gnt_lemma_frequency": 169
        },
        "decl2::χειμάρρους": {
          "type": "noun",
          "lexical_form": "χειμάρρους",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::χειμάρρους::nominative.singular",
            "decl2::χειμάρρους::genitive.singular",
            "decl2::χειμάρρους::dative.singular",
            "decl2::χειμάρρους::accusative.singular",
            "decl2::χειμάρρους::vocative.singular",
            "decl2::χειμάρρους::nominative.plural",
            "decl2::χειμάρρους::genitive.plural",
            "decl2::χειμάρρους::dative.plural",
            "decl2::χειμάρρους::accusative.plural"
          ]
        },
        "decl2::ὀστοῦν": {
          "type": "noun",
          "lexical_form": "ὀστοῦν",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::ὀστοῦν::nominative.singular",
            "decl2::ὀστοῦν::genitive.singular",
            "decl2::ὀστοῦν::dative.singular",
            "decl2::ὀστοῦν::accusative.singular",
            "decl2::ὀστοῦν::vocative.singular",
            "decl2::ὀστοῦν::nominative.plural",
            "decl2::ὀστοῦν::genitive.plural",
            "decl2::ὀστοῦν::dative.plural",
            "decl2::ὀστοῦν::accusative.plural"
          ]
        },
        "decl2::κῶς": {
          "type": "noun",
          "lexical_form": "κῶς",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::κῶς::nominative.singular",
            "decl2::κῶς::genitive.singular",
            "decl2::κῶς::dative.singular",
            "decl2::κῶς::vocative.singular"
          ]
        }
      },
      "difficulty_tier": 1,
      "teaching_note": "Taught before the first declension because its endings are the ones the article and the 2-1-2 adjective reuse. Both drill lexemes were confirmed against the corpus to inflect exactly like λόγος.",
      "drill_lexemes": [
        "θεός",
        "ἄνθρωπος"
      ]
    },
    "paradigm": {
      "type": "noun",
      "lexical_form": "λόγος",
      "source": [
        {
          "resource": "BBGG",
          "chapter": "Appendix",
          "header": "Appendix",
          "page": null
        }
      ],
      "slots": [
        "decl2::λόγος::nominative.singular",
        "decl2::λόγος::genitive.singular",
        "decl2::λόγος::dative.singular",
        "decl2::λόγος::accusative.singular",
        "decl2::λόγος::vocative.singular",
        "decl2::λόγος::nominative.plural",
        "decl2::λόγος::genitive.plural",
        "decl2::λόγος::dative.plural",
        "decl2::λόγος::accusative.plural"
      ],
      "gnt_lemma_frequency": 331
    }
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with an adverbial dependent clause: comparative, kathos hos indicative",
      "formation": "καθώς plus the indicative. καθάπερ, οὕτως, ὡς and ὡσαύτως head the same kind of clause, as does the relative adjective ὅσος.",
      "function": "Sets one idea alongside another as an analogy, or says how something was done. Render with 'as', 'just as', 'in the same way' or 'thus'.",
      "syntactic_category": "Comparative (manner) - a syntactic usage, under Conjunctions > Adverbial Functions. Syntactic explanation: as, just as, in the same way, thus, or in this manner (suggests an analogy or comparison between the connected ideas or tells how something is to be done); καθάπερ, καθώς, οὕτως, ὡς, ὡσαύτως, ὡσεί, and ὥσπερ.",
      "position": "after the main clause by default; before it when you mean to give it emphasis"
    },
    "also_include": [],
    "setting_options": {
      "s156": "A household hurries to be ready before the guests arrive for a betrothal feast.",
      "s172": "A wine jar in the cellar is found empty and no one admits to it."
    }
  }
}
```

### `decl2::λόγος::dative.singular`

```json
{
  "item": {
    "item": {
      "key": "decl2::λόγος::dative.singular",
      "parent": "decl2::λόγος",
      "rule": "decl2",
      "form": "λόγῳ",
      "parsing": "dative singular",
      "features": {
        "case": "dative",
        "number": "singular"
      },
      "lexical_form": "λόγος"
    },
    "rule": {
      "name": "Second Declension Nouns",
      "sequence": 9,
      "pos_lex_category": "noun",
      "morph_rule_description": "Stems ending in omicron. Masculine nouns take -ος in the nominative singular, neuter nouns -ον, and the two differ only in the nominative and accusative.",
      "paradigms": {
        "decl2::λόγος": {
          "type": "noun",
          "lexical_form": "λόγος",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::λόγος::nominative.singular",
            "decl2::λόγος::genitive.singular",
            "decl2::λόγος::dative.singular",
            "decl2::λόγος::accusative.singular",
            "decl2::λόγος::vocative.singular",
            "decl2::λόγος::nominative.plural",
            "decl2::λόγος::genitive.plural",
            "decl2::λόγος::dative.plural",
            "decl2::λόγος::accusative.plural"
          ],
          "gnt_lemma_frequency": 331
        },
        "decl2::ὁδός": {
          "type": "noun",
          "lexical_form": "ὁδός",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::ὁδός::nominative.singular",
            "decl2::ὁδός::genitive.singular",
            "decl2::ὁδός::dative.singular",
            "decl2::ὁδός::accusative.singular",
            "decl2::ὁδός::vocative.singular",
            "decl2::ὁδός::nominative.plural",
            "decl2::ὁδός::genitive.plural",
            "decl2::ὁδός::dative.plural",
            "decl2::ὁδός::accusative.plural"
          ],
          "gnt_lemma_frequency": 101
        },
        "decl2::ἔργον": {
          "type": "noun",
          "lexical_form": "ἔργον",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::ἔργον::nominative.singular",
            "decl2::ἔργον::genitive.singular",
            "decl2::ἔργον::dative.singular",
            "decl2::ἔργον::accusative.singular",
            "decl2::ἔργον::vocative.singular",
            "decl2::ἔργον::nominative.plural",
            "decl2::ἔργον::genitive.plural",
            "decl2::ἔργον::dative.plural",
            "decl2::ἔργον::accusative.plural"
          ],
          "gnt_lemma_frequency": 169
        },
        "decl2::χειμάρρους": {
          "type": "noun",
          "lexical_form": "χειμάρρους",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::χειμάρρους::nominative.singular",
            "decl2::χειμάρρους::genitive.singular",
            "decl2::χειμάρρους::dative.singular",
            "decl2::χειμάρρους::accusative.singular",
            "decl2::χειμάρρους::vocative.singular",
            "decl2::χειμάρρους::nominative.plural",
            "decl2::χειμάρρους::genitive.plural",
            "decl2::χειμάρρους::dative.plural",
            "decl2::χειμάρρους::accusative.plural"
          ]
        },
        "decl2::ὀστοῦν": {
          "type": "noun",
          "lexical_form": "ὀστοῦν",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::ὀστοῦν::nominative.singular",
            "decl2::ὀστοῦν::genitive.singular",
            "decl2::ὀστοῦν::dative.singular",
            "decl2::ὀστοῦν::accusative.singular",
            "decl2::ὀστοῦν::vocative.singular",
            "decl2::ὀστοῦν::nominative.plural",
            "decl2::ὀστοῦν::genitive.plural",
            "decl2::ὀστοῦν::dative.plural",
            "decl2::ὀστοῦν::accusative.plural"
          ]
        },
        "decl2::κῶς": {
          "type": "noun",
          "lexical_form": "κῶς",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::κῶς::nominative.singular",
            "decl2::κῶς::genitive.singular",
            "decl2::κῶς::dative.singular",
            "decl2::κῶς::vocative.singular"
          ]
        }
      },
      "difficulty_tier": 1,
      "teaching_note": "Taught before the first declension because its endings are the ones the article and the 2-1-2 adjective reuse. Both drill lexemes were confirmed against the corpus to inflect exactly like λόγος.",
      "drill_lexemes": [
        "θεός",
        "ἄνθρωπος"
      ]
    },
    "paradigm": {
      "type": "noun",
      "lexical_form": "λόγος",
      "source": [
        {
          "resource": "BBGG",
          "chapter": "Appendix",
          "header": "Appendix",
          "page": null
        }
      ],
      "slots": [
        "decl2::λόγος::nominative.singular",
        "decl2::λόγος::genitive.singular",
        "decl2::λόγος::dative.singular",
        "decl2::λόγος::accusative.singular",
        "decl2::λόγος::vocative.singular",
        "decl2::λόγος::nominative.plural",
        "decl2::λόγος::genitive.plural",
        "decl2::λόγος::dative.plural",
        "decl2::λόγος::accusative.plural"
      ],
      "gnt_lemma_frequency": 331
    }
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with a relative clause: substantival, subjunctive",
      "formation": "An indefinite relative clause: ὅστις with ἄν or ἐάν, or ὅς (δʼ) ἄν, plus the subjunctive.",
      "function": "Points to an unspecified person, group, event or action - 'whoever', 'whatever'. There is no antecedent. Translate as though it were indicative: the uncertainty is about who, not about whether.",
      "syntactic_category": "Subjunctive in Indefinite Relative Clause - a syntactic usage, under Moods > Subjunctive > In Dependent (Subordinate) Clauses. Syntactic explanation: after ὅστις (ἄν/ἐάν) or ὅς (δʼ) ἄν; construction indicates a generic or indefinite subject; translate like an indicative (since the contingency is of the person, not the action).",
      "position": "after the main clause by default; before it when you mean to give it emphasis",
      "paradigm": {
        "name": "Relative Pronoun",
        "forms": {
          "ὅς": {
            "nominative masculine singular": "ὅς",
            "genitive masculine singular": "οὗ",
            "dative masculine singular": "ᾧ",
            "accusative masculine singular": "ὅν",
            "nominative masculine plural": "οἵ",
            "genitive masculine plural": "ὧν",
            "dative masculine plural": "οἷς",
            "accusative masculine plural": "οὕς"
          },
          "ἥ": {
            "nominative feminine singular": "ἥ",
            "genitive feminine singular": "ἧς",
            "dative feminine singular": "ῇ",
            "accusative feminine singular": "ἥν",
            "nominative feminine plural": "αἵ",
            "genitive feminine plural": "ὧν",
            "dative feminine plural": "αἷς",
            "accusative feminine plural": "ἅς"
          },
          "ὅ": {
            "nominative neuter singular": "ὅ",
            "genitive neuter singular": "οὗ",
            "dative neuter singular": "ᾧ",
            "accusative neuter singular": "ὅ",
            "nominative neuter plural": "ἅ",
            "genitive neuter plural": "ὧν",
            "dative neuter plural": "οἷς",
            "accusative neuter plural": "ἅ"
          }
        }
      }
    },
    "also_include": [],
    "setting_options": {
      "s113": "A cook is punished for burning a feast meant for important guests.",
      "s112": "A servant carries a lamp ahead of his master along a dark street."
    }
  }
}
```

### `decl2::λόγος::accusative.plural`

```json
{
  "item": {
    "item": {
      "key": "decl2::λόγος::accusative.plural",
      "parent": "decl2::λόγος",
      "rule": "decl2",
      "form": "λόγους",
      "parsing": "accusative plural",
      "features": {
        "case": "accusative",
        "number": "plural"
      },
      "lexical_form": "λόγος"
    },
    "rule": {
      "name": "Second Declension Nouns",
      "sequence": 9,
      "pos_lex_category": "noun",
      "morph_rule_description": "Stems ending in omicron. Masculine nouns take -ος in the nominative singular, neuter nouns -ον, and the two differ only in the nominative and accusative.",
      "paradigms": {
        "decl2::λόγος": {
          "type": "noun",
          "lexical_form": "λόγος",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::λόγος::nominative.singular",
            "decl2::λόγος::genitive.singular",
            "decl2::λόγος::dative.singular",
            "decl2::λόγος::accusative.singular",
            "decl2::λόγος::vocative.singular",
            "decl2::λόγος::nominative.plural",
            "decl2::λόγος::genitive.plural",
            "decl2::λόγος::dative.plural",
            "decl2::λόγος::accusative.plural"
          ],
          "gnt_lemma_frequency": 331
        },
        "decl2::ὁδός": {
          "type": "noun",
          "lexical_form": "ὁδός",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::ὁδός::nominative.singular",
            "decl2::ὁδός::genitive.singular",
            "decl2::ὁδός::dative.singular",
            "decl2::ὁδός::accusative.singular",
            "decl2::ὁδός::vocative.singular",
            "decl2::ὁδός::nominative.plural",
            "decl2::ὁδός::genitive.plural",
            "decl2::ὁδός::dative.plural",
            "decl2::ὁδός::accusative.plural"
          ],
          "gnt_lemma_frequency": 101
        },
        "decl2::ἔργον": {
          "type": "noun",
          "lexical_form": "ἔργον",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::ἔργον::nominative.singular",
            "decl2::ἔργον::genitive.singular",
            "decl2::ἔργον::dative.singular",
            "decl2::ἔργον::accusative.singular",
            "decl2::ἔργον::vocative.singular",
            "decl2::ἔργον::nominative.plural",
            "decl2::ἔργον::genitive.plural",
            "decl2::ἔργον::dative.plural",
            "decl2::ἔργον::accusative.plural"
          ],
          "gnt_lemma_frequency": 169
        },
        "decl2::χειμάρρους": {
          "type": "noun",
          "lexical_form": "χειμάρρους",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::χειμάρρους::nominative.singular",
            "decl2::χειμάρρους::genitive.singular",
            "decl2::χειμάρρους::dative.singular",
            "decl2::χειμάρρους::accusative.singular",
            "decl2::χειμάρρους::vocative.singular",
            "decl2::χειμάρρους::nominative.plural",
            "decl2::χειμάρρους::genitive.plural",
            "decl2::χειμάρρους::dative.plural",
            "decl2::χειμάρρους::accusative.plural"
          ]
        },
        "decl2::ὀστοῦν": {
          "type": "noun",
          "lexical_form": "ὀστοῦν",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::ὀστοῦν::nominative.singular",
            "decl2::ὀστοῦν::genitive.singular",
            "decl2::ὀστοῦν::dative.singular",
            "decl2::ὀστοῦν::accusative.singular",
            "decl2::ὀστοῦν::vocative.singular",
            "decl2::ὀστοῦν::nominative.plural",
            "decl2::ὀστοῦν::genitive.plural",
            "decl2::ὀστοῦν::dative.plural",
            "decl2::ὀστοῦν::accusative.plural"
          ]
        },
        "decl2::κῶς": {
          "type": "noun",
          "lexical_form": "κῶς",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix",
              "page": null
            }
          ],
          "slots": [
            "decl2::κῶς::nominative.singular",
            "decl2::κῶς::genitive.singular",
            "decl2::κῶς::dative.singular",
            "decl2::κῶς::vocative.singular"
          ]
        }
      },
      "difficulty_tier": 1,
      "teaching_note": "Taught before the first declension because its endings are the ones the article and the 2-1-2 adjective reuse. Both drill lexemes were confirmed against the corpus to inflect exactly like λόγος.",
      "drill_lexemes": [
        "θεός",
        "ἄνθρωπος"
      ]
    },
    "paradigm": {
      "type": "noun",
      "lexical_form": "λόγος",
      "source": [
        {
          "resource": "BBGG",
          "chapter": "Appendix",
          "header": "Appendix",
          "page": null
        }
      ],
      "slots": [
        "decl2::λόγος::nominative.singular",
        "decl2::λόγος::genitive.singular",
        "decl2::λόγος::dative.singular",
        "decl2::λόγος::accusative.singular",
        "decl2::λόγος::vocative.singular",
        "decl2::λόγος::nominative.plural",
        "decl2::λόγος::genitive.plural",
        "decl2::λόγος::dative.plural",
        "decl2::λόγος::accusative.plural"
      ],
      "gnt_lemma_frequency": 331
    }
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "two independent clauses joined by a coordinating conjunction",
      "formation": "A coordinating conjunction between two independent clauses. Connective: καί, δέ. Contrastive: ἀλλά, δέ, πλήν. Correlative: μέν … δέ, καί … καί. Inferential: οὖν, ἄρα, διό. Explanatory: γάρ. Disjunctive: ἤ.",
      "function": "Carries the movement of thought from one clause to the next by naming the logical relation between them. Both clauses stay independent.",
      "note": "γάρ, δέ, οὖν and μέν are postpositive and cannot stand first in their clause. See the hard constraints under WORD ORDER.",
      "syntactic_category": "Connective (continuative, coordinate) - a syntactic usage, under Conjunctions. Syntactic explanation: and, also (if emphatic [adjunctive]); (connects an additional element to a discussion); καί and δέ."
    },
    "also_include": [],
    "setting_options": {
      "s135": "Travellers shelter from the rain under a rock overhang and share what food they have.",
      "s206": "A village grows into a town once the new road is built."
    }
  }
}
```

### `pres-act-ind::λύω::first_person.singular`

```json
{
  "item": {
    "item": {
      "key": "pres-act-ind::λύω::first_person.singular",
      "parent": "pres-act-ind::λύω",
      "rule": "pres-act-ind",
      "form": "λύω",
      "parsing": "present active indicative 1st person singular",
      "features": {
        "person": "first_person",
        "number": "singular",
        "tense": "present",
        "voice": "active",
        "mood": "indicative"
      },
      "lexical_form": "λύω"
    },
    "rule": {
      "name": "Present Active Indicative",
      "sequence": 153,
      "pos_lex_category": "verb",
      "morph_rule_description": "Unaugmented present stem, connecting vowel omicron or epsilon, primary active endings. This is the precedent every other verbal form is measured against.",
      "paradigms": {
        "pres-act-ind::λύω": {
          "type": "verb",
          "lexical_form": "λύω",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Overview of Indicative",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::λύω::first_person.singular",
            "pres-act-ind::λύω::second_person.singular",
            "pres-act-ind::λύω::third_person.singular",
            "pres-act-ind::λύω::first_person.plural",
            "pres-act-ind::λύω::second_person.plural",
            "pres-act-ind::λύω::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "λύω",
          "stem_class": "thematic",
          "gnt_lemma_frequency": 42
        },
        "pres-act-ind::γεννῶ": {
          "type": "verb",
          "lexical_form": "γεννῶ",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::γεννῶ::first_person.singular",
            "pres-act-ind::γεννῶ::second_person.singular",
            "pres-act-ind::γεννῶ::third_person.singular",
            "pres-act-ind::γεννῶ::first_person.plural",
            "pres-act-ind::γεννῶ::second_person.plural",
            "pres-act-ind::γεννῶ::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "γεννάω",
          "stem_class": "contract -άω",
          "gnt_lemma_frequency": 97
        },
        "pres-act-ind::ποιῶ": {
          "type": "verb",
          "lexical_form": "ποιῶ",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::ποιῶ::first_person.singular",
            "pres-act-ind::ποιῶ::second_person.singular",
            "pres-act-ind::ποιῶ::third_person.singular",
            "pres-act-ind::ποιῶ::first_person.plural",
            "pres-act-ind::ποιῶ::second_person.plural",
            "pres-act-ind::ποιῶ::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "ποιέω",
          "stem_class": "contract -έω",
          "gnt_lemma_frequency": 566
        },
        "pres-act-ind::φανερῶ": {
          "type": "verb",
          "lexical_form": "φανερῶ",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::φανερῶ::first_person.singular",
            "pres-act-ind::φανερῶ::second_person.singular",
            "pres-act-ind::φανερῶ::third_person.singular",
            "pres-act-ind::φανερῶ::first_person.plural",
            "pres-act-ind::φανερῶ::second_person.plural",
            "pres-act-ind::φανερῶ::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "φανερόω",
          "stem_class": "contract -όω",
          "gnt_lemma_frequency": 49
        },
        "pres-act-ind::ἵστημι": {
          "type": "verb",
          "lexical_form": "ἵστημι",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::ἵστημι::first_person.singular",
            "pres-act-ind::ἵστημι::second_person.singular",
            "pres-act-ind::ἵστημι::third_person.singular",
            "pres-act-ind::ἵστημι::first_person.plural",
            "pres-act-ind::ἵστημι::second_person.plural",
            "pres-act-ind::ἵστημι::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "ἵστημι",
          "stem_class": "athematic",
          "gnt_lemma_frequency": 153
        },
        "pres-act-ind::τίθημι": {
          "type": "verb",
          "lexical_form": "τίθημι",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::τίθημι::first_person.singular",
            "pres-act-ind::τίθημι::second_person.singular",
            "pres-act-ind::τίθημι::third_person.singular",
            "pres-act-ind::τίθημι::first_person.plural",
            "pres-act-ind::τίθημι::second_person.plural",
            "pres-act-ind::τίθημι::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "τίθημι",
          "stem_class": "athematic",
          "gnt_lemma_frequency": 99
        },
        "pres-act-ind::δίδωμι": {
          "type": "verb",
          "lexical_form": "δίδωμι",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::δίδωμι::first_person.singular",
            "pres-act-ind::δίδωμι::second_person.singular",
            "pres-act-ind::δίδωμι::third_person.singular",
            "pres-act-ind::δίδωμι::first_person.plural",
            "pres-act-ind::δίδωμι::second_person.plural",
            "pres-act-ind::δίδωμι::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "δίδωμι",
          "stem_class": "athematic",
          "gnt_lemma_frequency": 414
        },
        "pres-act-ind::δείκνυμι": {
          "type": "verb",
          "lexical_form": "δείκνυμι",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::δείκνυμι::first_person.singular",
            "pres-act-ind::δείκνυμι::second_person.singular",
            "pres-act-ind::δείκνυμι::third_person.singular",
            "pres-act-ind::δείκνυμι::first_person.plural",
            "pres-act-ind::δείκνυμι::second_person.plural",
            "pres-act-ind::δείκνυμι::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "δείκνυμι",
          "stem_class": "athematic",
          "gnt_lemma_frequency": 33
        }
      },
      "difficulty_tier": 1,
      "teaching_note": "GrammarSummaries' Master Verb Chart supplies the recipe columns directly: no augment, present stem, no tense formative, ο/ε connecting vowel, primary active endings.",
      "morph_recipe": {
        "tense_stem": "present",
        "connecting_vowel": "ο/ε",
        "personal_endings": "primary_active"
      },
      "drill_lexemes": [
        "πιστεύω",
        "γράφω"
      ]
    },
    "paradigm": {
      "type": "verb",
      "lexical_form": "λύω",
      "source": [
        {
          "resource": "BBGG",
          "chapter": "Appendix",
          "header": "Overview of Indicative",
          "page": null
        }
      ],
      "slots": [
        "pres-act-ind::λύω::first_person.singular",
        "pres-act-ind::λύω::second_person.singular",
        "pres-act-ind::λύω::third_person.singular",
        "pres-act-ind::λύω::first_person.plural",
        "pres-act-ind::λύω::second_person.plural",
        "pres-act-ind::λύω::third_person.plural"
      ],
      "tense": "present",
      "aspect": "continuous",
      "voice": "active",
      "mood": "indicative",
      "lemma": "λύω",
      "stem_class": "thematic",
      "gnt_lemma_frequency": 42
    }
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "two independent clauses joined by a coordinating conjunction",
      "formation": "A coordinating conjunction between two independent clauses. Connective: καί, δέ. Contrastive: ἀλλά, δέ, πλήν. Correlative: μέν … δέ, καί … καί. Inferential: οὖν, ἄρα, διό. Explanatory: γάρ. Disjunctive: ἤ.",
      "function": "Carries the movement of thought from one clause to the next by naming the logical relation between them. Both clauses stay independent.",
      "note": "γάρ, δέ, οὖν and μέν are postpositive and cannot stand first in their clause. See the hard constraints under WORD ORDER.",
      "syntactic_category": "Connective (continuative, coordinate) - a syntactic usage, under Conjunctions. Syntactic explanation: and, also (if emphatic [adjunctive]); (connects an additional element to a discussion); καί and δέ."
    },
    "also_include": [],
    "setting_options": {
      "s106": "A tutor walks a wealthy boy to school and scolds him for dawdling.",
      "s080": "A farmer and his sons pray for rain after a dry winter."
    }
  }
}
```

### `pres-act-ind::λύω::second_person.plural`

```json
{
  "item": {
    "item": {
      "key": "pres-act-ind::λύω::second_person.plural",
      "parent": "pres-act-ind::λύω",
      "rule": "pres-act-ind",
      "form": "λύετε",
      "parsing": "present active indicative 2nd person plural",
      "features": {
        "person": "second_person",
        "number": "plural",
        "tense": "present",
        "voice": "active",
        "mood": "indicative"
      },
      "lexical_form": "λύω"
    },
    "rule": {
      "name": "Present Active Indicative",
      "sequence": 153,
      "pos_lex_category": "verb",
      "morph_rule_description": "Unaugmented present stem, connecting vowel omicron or epsilon, primary active endings. This is the precedent every other verbal form is measured against.",
      "paradigms": {
        "pres-act-ind::λύω": {
          "type": "verb",
          "lexical_form": "λύω",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Overview of Indicative",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::λύω::first_person.singular",
            "pres-act-ind::λύω::second_person.singular",
            "pres-act-ind::λύω::third_person.singular",
            "pres-act-ind::λύω::first_person.plural",
            "pres-act-ind::λύω::second_person.plural",
            "pres-act-ind::λύω::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "λύω",
          "stem_class": "thematic",
          "gnt_lemma_frequency": 42
        },
        "pres-act-ind::γεννῶ": {
          "type": "verb",
          "lexical_form": "γεννῶ",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::γεννῶ::first_person.singular",
            "pres-act-ind::γεννῶ::second_person.singular",
            "pres-act-ind::γεννῶ::third_person.singular",
            "pres-act-ind::γεννῶ::first_person.plural",
            "pres-act-ind::γεννῶ::second_person.plural",
            "pres-act-ind::γεννῶ::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "γεννάω",
          "stem_class": "contract -άω",
          "gnt_lemma_frequency": 97
        },
        "pres-act-ind::ποιῶ": {
          "type": "verb",
          "lexical_form": "ποιῶ",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::ποιῶ::first_person.singular",
            "pres-act-ind::ποιῶ::second_person.singular",
            "pres-act-ind::ποιῶ::third_person.singular",
            "pres-act-ind::ποιῶ::first_person.plural",
            "pres-act-ind::ποιῶ::second_person.plural",
            "pres-act-ind::ποιῶ::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "ποιέω",
          "stem_class": "contract -έω",
          "gnt_lemma_frequency": 566
        },
        "pres-act-ind::φανερῶ": {
          "type": "verb",
          "lexical_form": "φανερῶ",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::φανερῶ::first_person.singular",
            "pres-act-ind::φανερῶ::second_person.singular",
            "pres-act-ind::φανερῶ::third_person.singular",
            "pres-act-ind::φανερῶ::first_person.plural",
            "pres-act-ind::φανερῶ::second_person.plural",
            "pres-act-ind::φανερῶ::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "φανερόω",
          "stem_class": "contract -όω",
          "gnt_lemma_frequency": 49
        },
        "pres-act-ind::ἵστημι": {
          "type": "verb",
          "lexical_form": "ἵστημι",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::ἵστημι::first_person.singular",
            "pres-act-ind::ἵστημι::second_person.singular",
            "pres-act-ind::ἵστημι::third_person.singular",
            "pres-act-ind::ἵστημι::first_person.plural",
            "pres-act-ind::ἵστημι::second_person.plural",
            "pres-act-ind::ἵστημι::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "ἵστημι",
          "stem_class": "athematic",
          "gnt_lemma_frequency": 153
        },
        "pres-act-ind::τίθημι": {
          "type": "verb",
          "lexical_form": "τίθημι",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::τίθημι::first_person.singular",
            "pres-act-ind::τίθημι::second_person.singular",
            "pres-act-ind::τίθημι::third_person.singular",
            "pres-act-ind::τίθημι::first_person.plural",
            "pres-act-ind::τίθημι::second_person.plural",
            "pres-act-ind::τίθημι::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "τίθημι",
          "stem_class": "athematic",
          "gnt_lemma_frequency": 99
        },
        "pres-act-ind::δίδωμι": {
          "type": "verb",
          "lexical_form": "δίδωμι",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::δίδωμι::first_person.singular",
            "pres-act-ind::δίδωμι::second_person.singular",
            "pres-act-ind::δίδωμι::third_person.singular",
            "pres-act-ind::δίδωμι::first_person.plural",
            "pres-act-ind::δίδωμι::second_person.plural",
            "pres-act-ind::δίδωμι::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "δίδωμι",
          "stem_class": "athematic",
          "gnt_lemma_frequency": 414
        },
        "pres-act-ind::δείκνυμι": {
          "type": "verb",
          "lexical_form": "δείκνυμι",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::δείκνυμι::first_person.singular",
            "pres-act-ind::δείκνυμι::second_person.singular",
            "pres-act-ind::δείκνυμι::third_person.singular",
            "pres-act-ind::δείκνυμι::first_person.plural",
            "pres-act-ind::δείκνυμι::second_person.plural",
            "pres-act-ind::δείκνυμι::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "δείκνυμι",
          "stem_class": "athematic",
          "gnt_lemma_frequency": 33
        }
      },
      "difficulty_tier": 1,
      "teaching_note": "GrammarSummaries' Master Verb Chart supplies the recipe columns directly: no augment, present stem, no tense formative, ο/ε connecting vowel, primary active endings.",
      "morph_recipe": {
        "tense_stem": "present",
        "connecting_vowel": "ο/ε",
        "personal_endings": "primary_active"
      },
      "drill_lexemes": [
        "πιστεύω",
        "γράφω"
      ]
    },
    "paradigm": {
      "type": "verb",
      "lexical_form": "λύω",
      "source": [
        {
          "resource": "BBGG",
          "chapter": "Appendix",
          "header": "Overview of Indicative",
          "page": null
        }
      ],
      "slots": [
        "pres-act-ind::λύω::first_person.singular",
        "pres-act-ind::λύω::second_person.singular",
        "pres-act-ind::λύω::third_person.singular",
        "pres-act-ind::λύω::first_person.plural",
        "pres-act-ind::λύω::second_person.plural",
        "pres-act-ind::λύω::third_person.plural"
      ],
      "tense": "present",
      "aspect": "continuous",
      "voice": "active",
      "mood": "indicative",
      "lemma": "λύω",
      "stem_class": "thematic",
      "gnt_lemma_frequency": 42
    }
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with an adverbial dependent clause: causal, oti indicative",
      "formation": "ὅτι plus a verb in the indicative. γάρ, διότι, ἐπεί, ἐπειδή, ἐπειδήπερ, καθώς and ὡς can head the same kind of clause.",
      "function": "States the basis or ground on which the main clause rests. Render with 'because' or 'since'.",
      "syntactic_category": "Causal (Adverbial) - a syntactic usage, under Moods > Indicative > The Indicative with Ὃτι. Syntactic explanation: because (introduces a dependent causal clause).",
      "position": "after the main clause by default; before it when you mean to give it emphasis"
    },
    "also_include": [
      "Dative of Interest (including Advantage [commodi] and Disadvantage [incommodi]) - a syntactic usage, under Dative > Pure Dative Uses."
    ],
    "setting_options": {
      "s139": "A mule breaks loose in the market and scatters the fruit stalls.",
      "s100": "A doctor examines a slave for sale in the market and declares him sick."
    }
  }
}
```

### `pres-act-ind::λύω::third_person.plural`

```json
{
  "item": {
    "item": {
      "key": "pres-act-ind::λύω::third_person.plural",
      "parent": "pres-act-ind::λύω",
      "rule": "pres-act-ind",
      "form": "λύουσι(ν)",
      "parsing": "present active indicative 3rd person plural",
      "features": {
        "person": "third_person",
        "number": "plural",
        "tense": "present",
        "voice": "active",
        "mood": "indicative"
      },
      "lexical_form": "λύω"
    },
    "rule": {
      "name": "Present Active Indicative",
      "sequence": 153,
      "pos_lex_category": "verb",
      "morph_rule_description": "Unaugmented present stem, connecting vowel omicron or epsilon, primary active endings. This is the precedent every other verbal form is measured against.",
      "paradigms": {
        "pres-act-ind::λύω": {
          "type": "verb",
          "lexical_form": "λύω",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Overview of Indicative",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::λύω::first_person.singular",
            "pres-act-ind::λύω::second_person.singular",
            "pres-act-ind::λύω::third_person.singular",
            "pres-act-ind::λύω::first_person.plural",
            "pres-act-ind::λύω::second_person.plural",
            "pres-act-ind::λύω::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "λύω",
          "stem_class": "thematic",
          "gnt_lemma_frequency": 42
        },
        "pres-act-ind::γεννῶ": {
          "type": "verb",
          "lexical_form": "γεννῶ",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::γεννῶ::first_person.singular",
            "pres-act-ind::γεννῶ::second_person.singular",
            "pres-act-ind::γεννῶ::third_person.singular",
            "pres-act-ind::γεννῶ::first_person.plural",
            "pres-act-ind::γεννῶ::second_person.plural",
            "pres-act-ind::γεννῶ::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "γεννάω",
          "stem_class": "contract -άω",
          "gnt_lemma_frequency": 97
        },
        "pres-act-ind::ποιῶ": {
          "type": "verb",
          "lexical_form": "ποιῶ",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::ποιῶ::first_person.singular",
            "pres-act-ind::ποιῶ::second_person.singular",
            "pres-act-ind::ποιῶ::third_person.singular",
            "pres-act-ind::ποιῶ::first_person.plural",
            "pres-act-ind::ποιῶ::second_person.plural",
            "pres-act-ind::ποιῶ::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "ποιέω",
          "stem_class": "contract -έω",
          "gnt_lemma_frequency": 566
        },
        "pres-act-ind::φανερῶ": {
          "type": "verb",
          "lexical_form": "φανερῶ",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::φανερῶ::first_person.singular",
            "pres-act-ind::φανερῶ::second_person.singular",
            "pres-act-ind::φανερῶ::third_person.singular",
            "pres-act-ind::φανερῶ::first_person.plural",
            "pres-act-ind::φανερῶ::second_person.plural",
            "pres-act-ind::φανερῶ::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "φανερόω",
          "stem_class": "contract -όω",
          "gnt_lemma_frequency": 49
        },
        "pres-act-ind::ἵστημι": {
          "type": "verb",
          "lexical_form": "ἵστημι",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::ἵστημι::first_person.singular",
            "pres-act-ind::ἵστημι::second_person.singular",
            "pres-act-ind::ἵστημι::third_person.singular",
            "pres-act-ind::ἵστημι::first_person.plural",
            "pres-act-ind::ἵστημι::second_person.plural",
            "pres-act-ind::ἵστημι::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "ἵστημι",
          "stem_class": "athematic",
          "gnt_lemma_frequency": 153
        },
        "pres-act-ind::τίθημι": {
          "type": "verb",
          "lexical_form": "τίθημι",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::τίθημι::first_person.singular",
            "pres-act-ind::τίθημι::second_person.singular",
            "pres-act-ind::τίθημι::third_person.singular",
            "pres-act-ind::τίθημι::first_person.plural",
            "pres-act-ind::τίθημι::second_person.plural",
            "pres-act-ind::τίθημι::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "τίθημι",
          "stem_class": "athematic",
          "gnt_lemma_frequency": 99
        },
        "pres-act-ind::δίδωμι": {
          "type": "verb",
          "lexical_form": "δίδωμι",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::δίδωμι::first_person.singular",
            "pres-act-ind::δίδωμι::second_person.singular",
            "pres-act-ind::δίδωμι::third_person.singular",
            "pres-act-ind::δίδωμι::first_person.plural",
            "pres-act-ind::δίδωμι::second_person.plural",
            "pres-act-ind::δίδωμι::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "δίδωμι",
          "stem_class": "athematic",
          "gnt_lemma_frequency": 414
        },
        "pres-act-ind::δείκνυμι": {
          "type": "verb",
          "lexical_form": "δείκνυμι",
          "source": [
            {
              "resource": "BBGG",
              "chapter": "Appendix",
              "header": "Appendix (MBG)",
              "page": null
            }
          ],
          "slots": [
            "pres-act-ind::δείκνυμι::first_person.singular",
            "pres-act-ind::δείκνυμι::second_person.singular",
            "pres-act-ind::δείκνυμι::third_person.singular",
            "pres-act-ind::δείκνυμι::first_person.plural",
            "pres-act-ind::δείκνυμι::second_person.plural",
            "pres-act-ind::δείκνυμι::third_person.plural"
          ],
          "tense": "present",
          "aspect": "continuous",
          "voice": "active",
          "mood": "indicative",
          "lemma": "δείκνυμι",
          "stem_class": "athematic",
          "gnt_lemma_frequency": 33
        }
      },
      "difficulty_tier": 1,
      "teaching_note": "GrammarSummaries' Master Verb Chart supplies the recipe columns directly: no augment, present stem, no tense formative, ο/ε connecting vowel, primary active endings.",
      "morph_recipe": {
        "tense_stem": "present",
        "connecting_vowel": "ο/ε",
        "personal_endings": "primary_active"
      },
      "drill_lexemes": [
        "πιστεύω",
        "γράφω"
      ]
    },
    "paradigm": {
      "type": "verb",
      "lexical_form": "λύω",
      "source": [
        {
          "resource": "BBGG",
          "chapter": "Appendix",
          "header": "Overview of Indicative",
          "page": null
        }
      ],
      "slots": [
        "pres-act-ind::λύω::first_person.singular",
        "pres-act-ind::λύω::second_person.singular",
        "pres-act-ind::λύω::third_person.singular",
        "pres-act-ind::λύω::first_person.plural",
        "pres-act-ind::λύω::second_person.plural",
        "pres-act-ind::λύω::third_person.plural"
      ],
      "tense": "present",
      "aspect": "continuous",
      "voice": "active",
      "mood": "indicative",
      "lemma": "λύω",
      "stem_class": "thematic",
      "gnt_lemma_frequency": 42
    }
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with an adverbial dependent clause: causal, oti indicative",
      "formation": "ὅτι plus a verb in the indicative. γάρ, διότι, ἐπεί, ἐπειδή, ἐπειδήπερ, καθώς and ὡς can head the same kind of clause.",
      "function": "States the basis or ground on which the main clause rests. Render with 'because' or 'since'.",
      "syntactic_category": "Causal (Adverbial) - a syntactic usage, under Moods > Indicative > The Indicative with Ὃτι. Syntactic explanation: because (introduces a dependent causal clause).",
      "position": "after the main clause by default; before it when you mean to give it emphasis"
    },
    "also_include": [],
    "setting_options": {
      "s048": "A steward counts the household stores before winter and finds the oil jars half empty.",
      "s066": "A woman keeps watch at the bedside of her dying husband."
    }
  }
}
```

## vocabulary — `text_recall_vocabulary_g2e`

### `βαπτίζω`

```json
{
  "item": {
    "lemma": "βαπτίζω",
    "part_of_speech": "verb",
    "gloss": "dip, baptize",
    "frequency": 76,
    "lexical_entry": "βαπτίζω",
    "summary": "βαπτίζω: primary sense 53.41 (65 of 75 tagged occurrences, 53 Religious Activities / E Baptize). Secondary senses: 24.82 (5x), 53.49 (4x), 53.31 (1x)."
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with an adverbial dependent clause: conditional, second class",
      "formation": "Protasis: εἰ plus a secondary tense of the indicative, normally aorist or imperfect. Apodosis: usually ἄν with the indicative in the same secondary tense.",
      "function": "The speaker takes the condition as untrue and then says what would have been the case had it been true. Contrary to fact.",
      "syntactic_category": "Second Class Condition - a syntactic usage, under Conditional Sentences > II. Conditional Sentences in Greek (especially the NT). Syntactic explanation: the assumption of an untruth (for the sake of argument); protasis: εἰ + indicative of secondary tense (aorist or imperfect usually)/apodosis: ἄν (usually) + secondary tense in indicative (689, 694–96).",
      "position": "before the main clause by default; after it when you mean to give it emphasis",
      "paradigm": {
        "name": "Second Aorist Active Indicative",
        "forms": {
          "ἔλαβον (λαμβάνω, second aorist)": {
            "aorist active indicative 1st person singular": "ἔλαβον",
            "aorist active indicative 2nd person singular": "ἔλαβες",
            "aorist active indicative 3rd person singular": "ἔλαβε(ν)",
            "aorist active indicative 1st person plural": "ἐλάβομεν",
            "aorist active indicative 2nd person plural": "ἐλάβετε",
            "aorist active indicative 3rd person plural": "ἔλαβον"
          },
          "ἔβαλον (βάλλω, second aorist)": {
            "aorist active indicative 1st person singular": "ἔβαλον",
            "aorist active indicative 2nd person singular": "ἔβαλες",
            "aorist active indicative 3rd person singular": "ἔβαλε(ν)",
            "aorist active indicative 1st person plural": "ἐβάλομεν",
            "aorist active indicative 2nd person plural": "ἐβάλετε",
            "aorist active indicative 3rd person plural": "ἔβαλον"
          },
          "ἔστην (ἵστημι, root aorist)": {
            "aorist active indicative 1st person singular": "ἔστην",
            "aorist active indicative 2nd person singular": "ἔστης",
            "aorist active indicative 3rd person singular": "ἔστη",
            "aorist active indicative 1st person plural": "ἔστημεν",
            "aorist active indicative 2nd person plural": "ἔστητε",
            "aorist active indicative 3rd person plural": "ἔστησαν"
          },
          "ἔθην (τίθημι, root aorist)": {
            "aorist active indicative 1st person singular": "ἔθην",
            "aorist active indicative 2nd person singular": "ἔθης",
            "aorist active indicative 3rd person singular": "ἔθη",
            "aorist active indicative 1st person plural": "ἔθεμεν",
            "aorist active indicative 2nd person plural": "ἔθετε",
            "aorist active indicative 3rd person plural": "ἔθεσαν"
          },
          "ἔδων (δίδωμι, root aorist)": {
            "aorist active indicative 1st person singular": "ἔδων",
            "aorist active indicative 2nd person singular": "ἔδως",
            "aorist active indicative 3rd person singular": "ἔδω",
            "aorist active indicative 1st person plural": "ἔδομεν",
            "aorist active indicative 2nd person plural": "ἔδοτε",
            "aorist active indicative 3rd person plural": "ἔδοσαν"
          }
        }
      }
    },
    "also_include": [
      "Intensive Perfect (a.k.a. Resultative Perfect) - a syntactic usage, under Tense > Perfect. Syntactic explanation: emphasizes the results or present state produced by a past action (often best translated like English present); frequent with stative verbs."
    ],
    "setting_options": {
      "s077": "An old man teaches his grandson the blessing said before meals.",
      "s080": "A farmer and his sons pray for rain after a dry winter."
    }
  }
}
```

### `κράζω`

```json
{
  "item": {
    "lemma": "κράζω",
    "part_of_speech": "verb",
    "gloss": "cry out, cry, call out",
    "frequency": 55,
    "lexical_entry": "κράζω",
    "summary": "κράζω: primary sense 33.83 (54 of 54 tagged occurrences, 33 Communication / F Speak, Talk). No secondary senses attested."
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "two independent clauses joined by a coordinating conjunction",
      "formation": "A coordinating conjunction between two independent clauses. Connective: καί, δέ. Contrastive: ἀλλά, δέ, πλήν. Correlative: μέν … δέ, καί … καί. Inferential: οὖν, ἄρα, διό. Explanatory: γάρ. Disjunctive: ἤ.",
      "function": "Carries the movement of thought from one clause to the next by naming the logical relation between them. Both clauses stay independent.",
      "note": "γάρ, δέ, οὖν and μέν are postpositive and cannot stand first in their clause. See the hard constraints under WORD ORDER.",
      "syntactic_category": "Connective (continuative, coordinate) - a syntactic usage, under Conjunctions. Syntactic explanation: and, also (if emphatic [adjunctive]); (connects an additional element to a discussion); καί and δέ."
    },
    "also_include": [
      "Explanatory - a syntactic usage, under Conjunctions. Syntactic explanation: for, you see, or that is, namely (conjunction indicates additional information being given to what has been described); γάρ, δέ, εἰ (after verbs of emotion), and καί."
    ],
    "setting_options": {
      "s020": "An innkeeper and a traveller quarrel over the bill for feeding the traveller's mules.",
      "s144": "An old woman tells her grandchildren about her own wedding day."
    }
  }
}
```

### `διώκω`

```json
{
  "item": {
    "lemma": "διώκω",
    "part_of_speech": "verb",
    "gloss": "hasten; pursue, persecute",
    "frequency": 45,
    "lexical_entry": "διώκω",
    "summary": "διώκω: primary sense 39.45 (30 of 47 tagged occurrences, 39 Hostility, Strife / I Persecution). Secondary senses: 68.66 (9x), 15.158 (5x), 15.223 (2x), 89.56 (1x)."
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with a relative clause: adjectival",
      "formation": "Relative pronoun agreeing with its antecedent in number and gender, its case set by its role inside the relative clause. It follows its referent.",
      "function": "Attributive only - it describes, explains or narrows the substantive it attaches to.",
      "syntactic_category": "Relative Pronouns - a syntactic usage, under Pronouns > Semantic Categories. Syntactic explanation: ὅς and ὅστις labeled relative pronouns because they relate to more than one clause.",
      "position": "after the main clause by default; before it when you mean to give it emphasis",
      "paradigm": {
        "name": "Relative Pronoun",
        "forms": {
          "ὅς": {
            "nominative masculine singular": "ὅς",
            "genitive masculine singular": "οὗ",
            "dative masculine singular": "ᾧ",
            "accusative masculine singular": "ὅν",
            "nominative masculine plural": "οἵ",
            "genitive masculine plural": "ὧν",
            "dative masculine plural": "οἷς",
            "accusative masculine plural": "οὕς"
          },
          "ἥ": {
            "nominative feminine singular": "ἥ",
            "genitive feminine singular": "ἧς",
            "dative feminine singular": "ῇ",
            "accusative feminine singular": "ἥν",
            "nominative feminine plural": "αἵ",
            "genitive feminine plural": "ὧν",
            "dative feminine plural": "αἷς",
            "accusative feminine plural": "ἅς"
          },
          "ὅ": {
            "nominative neuter singular": "ὅ",
            "genitive neuter singular": "οὗ",
            "dative neuter singular": "ᾧ",
            "accusative neuter singular": "ὅ",
            "nominative neuter plural": "ἅ",
            "genitive neuter plural": "ὧν",
            "dative neuter plural": "οἷς",
            "accusative neuter plural": "ἅ"
          }
        }
      }
    },
    "also_include": [
      "Genitive of Relationship - a syntactic usage, under Genitive > Adjectival. Syntactic explanation: family relationship (subset of possessive)."
    ],
    "setting_options": {
      "s108": "An archer practises at a target while his friends mock him.",
      "s119": "Three families share an olive press and argue over whose turn it is."
    }
  }
}
```

### `θεραπεύω`

```json
{
  "item": {
    "lemma": "θεραπεύω",
    "part_of_speech": "verb",
    "gloss": "care for, heal",
    "frequency": 43,
    "lexical_entry": "θεραπεύω",
    "summary": "θεραπεύω: primary sense 23.139 (42 of 43 tagged occurrences, 23 Physiological Processes and States / H Health, Vigor, Strength). Secondary senses: 35.19 (1x)."
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a single main clause",
      "formation": "A single independent clause: nominative subject, finite verb, and an accusative direct object if the verb is transitive.",
      "function": "One unsubordinated assertion. Unmarked order is subject, then predicate, then complement."
    },
    "also_include": [
      "Condition - a syntactic usage, under Participle > Verbal Participles > Dependent Verbal Participles > Adverbial (or Circumstantial). Syntactic explanation: if (implies a condition on which the fulfillment of the idea indicated by the main verb depends)."
    ],
    "setting_options": {
      "s060": "A servant is sent to fetch a doctor in the middle of a storm.",
      "s130": "A guard dog barks all night and no one sleeps."
    }
  }
}
```

### `θύρα`

```json
{
  "item": {
    "lemma": "θύρα",
    "part_of_speech": "noun",
    "gloss": "door",
    "frequency": 39,
    "lexical_entry": "ἡ θύρα",
    "summary": "θύρα: primary sense 7.49 (29 of 44 tagged occurrences, 7 Constructions / C Parts and Areas of Buildings). Secondary senses: 7.39 (12x), 67.58 (3x)."
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with an adverbial dependent clause: causal, oti indicative",
      "formation": "ὅτι plus a verb in the indicative. γάρ, διότι, ἐπεί, ἐπειδή, ἐπειδήπερ, καθώς and ὡς can head the same kind of clause.",
      "function": "States the basis or ground on which the main clause rests. Render with 'because' or 'since'.",
      "syntactic_category": "Causal (Adverbial) - a syntactic usage, under Moods > Indicative > The Indicative with Ὃτι. Syntactic explanation: because (introduces a dependent causal clause).",
      "position": "after the main clause by default; before it when you mean to give it emphasis"
    },
    "also_include": [
      "Attributive Genitive - a syntactic usage, under Genitive > Adjectival. Syntactic explanation: specifies an attribute or innate quality of the head substantive; convert genitive into an attributive adjective."
    ],
    "setting_options": {
      "s102": "A fisherman's hut floods when the lake rises.",
      "s140": "A widow hires a man to mend her leaking roof before the rains."
    }
  }
}
```

### `ποιμήν`

```json
{
  "item": {
    "lemma": "ποιμήν",
    "part_of_speech": "noun",
    "gloss": "shepherd",
    "frequency": 18,
    "lexical_entry": "ὁ ποιμήν",
    "summary": "ποιμήν: primary sense 44.4 (12 of 18 tagged occurrences, 44 Animal Husbandry, Fishing / Overview). Secondary senses: 53.72 (6x)."
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "two independent clauses joined by a coordinating conjunction",
      "formation": "A coordinating conjunction between two independent clauses. Connective: καί, δέ. Contrastive: ἀλλά, δέ, πλήν. Correlative: μέν … δέ, καί … καί. Inferential: οὖν, ἄρα, διό. Explanatory: γάρ. Disjunctive: ἤ.",
      "function": "Carries the movement of thought from one clause to the next by naming the logical relation between them. Both clauses stay independent.",
      "note": "γάρ, δέ, οὖν and μέν are postpositive and cannot stand first in their clause. See the hard constraints under WORD ORDER.",
      "syntactic_category": "Connective (continuative, coordinate) - a syntactic usage, under Conjunctions. Syntactic explanation: and, also (if emphatic [adjunctive]); (connects an additional element to a discussion); καί and δέ."
    },
    "also_include": [],
    "setting_options": {
      "s005": "A shepherd boy counts the flock at dusk and finds one lamb lame.",
      "s004": "A fisherman's wife salts and packs the catch in jars to sell inland before it spoils."
    }
  }
}
```

### `σκότος`

```json
{
  "item": {
    "lemma": "σκότος",
    "part_of_speech": "noun",
    "gloss": "darkness",
    "frequency": 30,
    "lexical_entry": "τὸ σκότος",
    "summary": "σκότος: primary sense 88.125 (16 of 33 tagged occurrences, 88 Moral and Ethical Qualities and Related Behavior2 / O Bad, Evil, Harmful, Damaging). Secondary senses: 14.53 (13x), 1.23 (3x), 1.24 (1x)."
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with an adverbial dependent clause: causal, infinitive",
      "formation": "διὰ τό followed by an infinitive.",
      "function": "Gives the reason the controlling verb's action happened. Render it with 'because' plus a finite verb in English.",
      "syntactic_category": "Cause - a syntactic usage, under Infinitive > Adverbial. Syntactic explanation: διὰ τό + infinitive; indicates the reason for the action of the controlling verb; translate because + appropriate finite verb.",
      "position": "after the main clause by default; before it when you mean to give it emphasis",
      "paradigm": {
        "name": "Second Aorist Active Infinitive",
        "forms": {
          "λαβεῖν (λαμβάνω, second aorist)": {
            "aorist active infinitive": "λαβεῖν"
          },
          "βαλεῖν (βάλλω, second aorist)": {
            "aorist active infinitive": "βαλεῖν"
          },
          "στῆναι (ἵστημι, root aorist)": {
            "aorist active infinitive": "στῆναι"
          },
          "θεῖναι (τίθημι, root aorist)": {
            "aorist active infinitive": "θεῖναι"
          },
          "δοῦναι (δίδωμι, root aorist)": {
            "aorist active infinitive": "δοῦναι"
          }
        }
      }
    },
    "also_include": [],
    "setting_options": {
      "s030": "A thief is caught climbing into a storeroom.",
      "s040": "A boy steals pomegranates from a neighbour's garden and is chased off by the dog."
    }
  }
}
```

### `μάχαιρα`

```json
{
  "item": {
    "lemma": "μάχαιρα",
    "part_of_speech": "noun",
    "gloss": "sword",
    "frequency": 29,
    "lexical_entry": "ἡ μάχαιρα",
    "summary": "μάχαιρα: primary sense 6.33 (26 of 30 tagged occurrences, 6 Artifacts,2 / G Weapons and Armor). Secondary senses: 39.25 (1x), 55.6 (1x), 20.68 (1x), 38.3 (1x)."
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with a relative clause: substantival, indicative, subject",
      "formation": "ὅ plus the indicative, with no antecedent, standing in the subject slot of the main verb.",
      "function": "The relative clause serves as the subject of the main verb.",
      "syntactic_category": "Omission of Antecedent - a syntactic usage, under Pronouns > Semantic Categories > Relative Pronouns > ὅς > “Unusual” Uses > Antecedent Complexities. Syntactic explanation: due to embedded demonstrative or poetry.",
      "position": "after the main clause by default; before it when you mean to give it emphasis",
      "paradigm": {
        "name": "Relative Pronoun",
        "forms": {
          "ὅς": {
            "nominative masculine singular": "ὅς",
            "genitive masculine singular": "οὗ",
            "dative masculine singular": "ᾧ",
            "accusative masculine singular": "ὅν",
            "nominative masculine plural": "οἵ",
            "genitive masculine plural": "ὧν",
            "dative masculine plural": "οἷς",
            "accusative masculine plural": "οὕς"
          },
          "ἥ": {
            "nominative feminine singular": "ἥ",
            "genitive feminine singular": "ἧς",
            "dative feminine singular": "ῇ",
            "accusative feminine singular": "ἥν",
            "nominative feminine plural": "αἵ",
            "genitive feminine plural": "ὧν",
            "dative feminine plural": "αἷς",
            "accusative feminine plural": "ἅς"
          },
          "ὅ": {
            "nominative neuter singular": "ὅ",
            "genitive neuter singular": "οὗ",
            "dative neuter singular": "ᾧ",
            "accusative neuter singular": "ὅ",
            "nominative neuter plural": "ἅ",
            "genitive neuter plural": "ὧν",
            "dative neuter plural": "οἷς",
            "accusative neuter plural": "ἅ"
          }
        }
      }
    },
    "also_include": [],
    "setting_options": {
      "s013": "An old teacher tests his pupils on the letters they copied onto wax tablets.",
      "s028": "A merchant's ship waits in harbour for a favourable wind."
    }
  }
}
```

### `πιστός`

```json
{
  "item": {
    "lemma": "πιστός",
    "part_of_speech": "adj",
    "gloss": "trustworthy, faithful, believing",
    "frequency": 67,
    "lexical_entry": "πιστός, -ή, -όν",
    "summary": "πιστός: primary sense 31.87 (51 of 72 tagged occurrences, 31 Hold a View, Believe, Trust / I Trust, Rely). Secondary senses: 31.86 (12x), 71.17 (5x), 11.17 (2x), 31.103 (2x)."
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with a relative clause: substantival, subjunctive",
      "formation": "An indefinite relative clause: ὅστις with ἄν or ἐάν, or ὅς (δʼ) ἄν, plus the subjunctive.",
      "function": "Points to an unspecified person, group, event or action - 'whoever', 'whatever'. There is no antecedent. Translate as though it were indicative: the uncertainty is about who, not about whether.",
      "syntactic_category": "Subjunctive in Indefinite Relative Clause - a syntactic usage, under Moods > Subjunctive > In Dependent (Subordinate) Clauses. Syntactic explanation: after ὅστις (ἄν/ἐάν) or ὅς (δʼ) ἄν; construction indicates a generic or indefinite subject; translate like an indicative (since the contingency is of the person, not the action).",
      "position": "after the main clause by default; before it when you mean to give it emphasis",
      "paradigm": {
        "name": "Relative Pronoun",
        "forms": {
          "ὅς": {
            "nominative masculine singular": "ὅς",
            "genitive masculine singular": "οὗ",
            "dative masculine singular": "ᾧ",
            "accusative masculine singular": "ὅν",
            "nominative masculine plural": "οἵ",
            "genitive masculine plural": "ὧν",
            "dative masculine plural": "οἷς",
            "accusative masculine plural": "οὕς"
          },
          "ἥ": {
            "nominative feminine singular": "ἥ",
            "genitive feminine singular": "ἧς",
            "dative feminine singular": "ῇ",
            "accusative feminine singular": "ἥν",
            "nominative feminine plural": "αἵ",
            "genitive feminine plural": "ὧν",
            "dative feminine plural": "αἷς",
            "accusative feminine plural": "ἅς"
          },
          "ὅ": {
            "nominative neuter singular": "ὅ",
            "genitive neuter singular": "οὗ",
            "dative neuter singular": "ᾧ",
            "accusative neuter singular": "ὅ",
            "nominative neuter plural": "ἅ",
            "genitive neuter plural": "ὧν",
            "dative neuter plural": "οἷς",
            "accusative neuter plural": "ἅ"
          }
        }
      }
    },
    "also_include": [],
    "setting_options": {
      "s036": "Two merchants swear an oath over a disputed shipment of wool.",
      "s007": "A hired letter-writer in the market draws up a contract for two farmers who distrust each other."
    }
  }
}
```

### `εὐθέως`

```json
{
  "item": {
    "lemma": "εὐθέως",
    "part_of_speech": "adv",
    "gloss": "immediately, soon",
    "frequency": 33,
    "lexical_entry": "εὐθέως",
    "summary": "εὐθέως: primary sense 67.53 (33 of 33 tagged occurrences, 67 Time / B A Point of Time with Reference to Other Points of Time: Before, Long Ago, Now, At the Same Time, When, About, After). No secondary senses attested."
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "two independent clauses joined by a coordinating conjunction",
      "formation": "A coordinating conjunction between two independent clauses. Connective: καί, δέ. Contrastive: ἀλλά, δέ, πλήν. Correlative: μέν … δέ, καί … καί. Inferential: οὖν, ἄρα, διό. Explanatory: γάρ. Disjunctive: ἤ.",
      "function": "Carries the movement of thought from one clause to the next by naming the logical relation between them. Both clauses stay independent.",
      "note": "γάρ, δέ, οὖν and μέν are postpositive and cannot stand first in their clause. See the hard constraints under WORD ORDER.",
      "syntactic_category": "Connective (continuative, coordinate) - a syntactic usage, under Conjunctions. Syntactic explanation: and, also (if emphatic [adjunctive]); (connects an additional element to a discussion); καί and δέ."
    },
    "also_include": [],
    "setting_options": {
      "s030": "A thief is caught climbing into a storeroom.",
      "s017": "A baker's oven cracks on the morning of a festival."
    }
  }
}
```

## syntax — `function_recall_syntax_g2e`

### `genitive/adjectival/descriptive-genitive`

```json
{
  "item": {
    "item": {
      "key": "genitive/adjectival/descriptive-genitive",
      "display_name": "Descriptive Genitive",
      "description": "characterized by, described by"
    },
    "ancestors": [
      {
        "display_name": "Genitive",
        "description": "qualification & [occasionally] separation"
      },
      {
        "display_name": "Adjectival",
        "description": null
      }
    ],
    "sibling_usages": {
      "genitive/adjectival/possessive-genitive": {
        "display_name": "Possessive Genitive",
        "description": "belonging to, possessed by"
      },
      "genitive/adjectival/genitive-relationship": {
        "display_name": "Genitive of Relationship",
        "description": "family relationship (subset of possessive)"
      },
      "genitive/adjectival/partitive-genitive-wholative": {
        "display_name": "Partitive Genitive (“Wholative”)",
        "description": "denotes the whole of which the head noun is a part—which is a part of"
      },
      "genitive/adjectival/attributive-genitive": {
        "display_name": "Attributive Genitive",
        "description": "specifies an attribute or innate quality of the head substantive; convert genitive into an attributive adjective"
      },
      "genitive/adjectival/attributed-genitive": {
        "display_name": "Attributed Genitive",
        "description": "semantically opposite of attributive genitive; convert head noun into adjective modifying the genitive noun"
      },
      "genitive/adjectival/genitive-material": {
        "display_name": "Genitive of Material",
        "description": "made out of, consisting of"
      },
      "genitive/adjectival/genitive-content": {
        "display_name": "Genitive of Content",
        "description": "full of, containing (related to noun or verb)"
      },
      "genitive/adjectival/genitive-simple-apposition": {
        "display_name": "Genitive in Simple Apposition",
        "description": "genitive substantive adjacent to another genitive substantive, referring to the same thing/person—namely, which is"
      },
      "genitive/adjectival/genitive-apposition-epexegetical": {
        "display_name": "Genitive of Apposition (Epexegetical)",
        "description": "genitive states a specific example of which the head noun names a category—namely, which is"
      },
      "genitive/adjectival/genitive-destination-k-direction-purpose": {
        "display_name": "Genitive of Destination (a.k.a. Direction or Purpose)",
        "description": "for the purpose of, destined for, toward, or into"
      },
      "genitive/adjectival/predicate-genitive": {
        "display_name": "Predicate Genitive",
        "description": "simple apposition in genitive case made emphatic by participial form of the equative verb"
      },
      "genitive/adjectival/genitive-subordination": {
        "display_name": "Genitive of Subordination",
        "description": "specifies that which is subordinated to or under the dominion of the head noun—over"
      },
      "genitive/adjectival/genitive-production-producer": {
        "display_name": "Genitive of Production/Producer",
        "description": "genitive produces the noun to which it stands related—produced by"
      },
      "genitive/adjectival/genitive-product": {
        "display_name": "Genitive of Product",
        "description": "genitive is the product of the noun to which it stands related—which produces"
      }
    },
    "lexical_options": [
      "λίθος",
      "ὕδωρ",
      "οἰκία"
    ]
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with an adverbial dependent clause: causal, infinitive",
      "formation": "διὰ τό followed by an infinitive.",
      "function": "Gives the reason the controlling verb's action happened. Render it with 'because' plus a finite verb in English.",
      "syntactic_category": "Cause - a syntactic usage, under Infinitive > Adverbial. Syntactic explanation: διὰ τό + infinitive; indicates the reason for the action of the controlling verb; translate because + appropriate finite verb.",
      "position": "after the main clause by default; before it when you mean to give it emphasis",
      "paradigm": {
        "name": "Present Active Infinitive",
        "forms": {
          "λύειν (λύω, thematic)": {
            "present active infinitive": "λύειν"
          },
          "μένειν (μένω, liquid)": {
            "present active infinitive": "μένειν"
          },
          "γεννᾶν (γεννάω, contract -άω)": {
            "present active infinitive": "γεννᾶν"
          },
          "ποιεῖν (ποιέω, contract -έω)": {
            "present active infinitive": "ποιεῖν"
          },
          "φανεροῦν (φανερόω, contract -όω)": {
            "present active infinitive": "φανεροῦν"
          },
          "ἱστάναι (ἵστημι, athematic)": {
            "present active infinitive": "ἱστάναι"
          },
          "τιθέναι (τίθημι, athematic)": {
            "present active infinitive": "τιθέναι"
          },
          "διδόναι (δίδωμι, athematic)": {
            "present active infinitive": "διδόναι"
          },
          "δεικνύναι (δείκνυμι, athematic)": {
            "present active infinitive": "δεικνύναι"
          }
        }
      }
    },
    "also_include": [
      "Nominative Absolute - a syntactic usage, under Nominative > Grammatically Independent Uses of the Nominative. Syntactic explanation: in introductory material (not sentences)."
    ],
    "setting_options": {
      "s074": "Pilgrims camp outside the city walls during a festival and quarrel over space.",
      "s020": "An innkeeper and a traveller quarrel over the bill for feeding the traveller's mules."
    }
  }
}
```

### `dative/pure-dative-uses/dative-indirect-object`

```json
{
  "item": {
    "item": {
      "key": "dative/pure-dative-uses/dative-indirect-object",
      "display_name": "Dative Indirect Object",
      "description": "dative noun is that to or for which the action of a transitive verb is performed—to, for"
    },
    "ancestors": [
      {
        "display_name": "Dative",
        "description": "personal interest, reference, position, & means"
      },
      {
        "display_name": "Pure Dative Uses",
        "description": null
      }
    ],
    "sibling_usages": {
      "dative/pure-dative-uses/dative-interest-including-advantage-commodi-disadvantage-inc": {
        "display_name": "Dative of Interest (including Advantage [commodi] and Disadvantage [incommodi])",
        "description": null
      },
      "dative/pure-dative-uses/dative-reference-respect": {
        "display_name": "Dative of Reference/Respect",
        "description": "with reference to"
      },
      "dative/pure-dative-uses/ethical-dative": {
        "display_name": "Ethical Dative",
        "description": "the person whose feelings or viewpoint are intimately tied to the action—as far as I am concerned, in my opinion"
      },
      "dative/pure-dative-uses/dative-destination": {
        "display_name": "Dative of Destination",
        "description": "the “to” idea when a nontransitive verb is used"
      },
      "dative/pure-dative-uses/dative-recipient": {
        "display_name": "Dative of Recipient",
        "description": "would be an indirect object, but it appears in verbless constructions (such as in titles and salutations)"
      },
      "dative/pure-dative-uses/dative-possession": {
        "display_name": "Dative of Possession",
        "description": "that to which the subject of an equative verb belongs—belonging to"
      },
      "dative/pure-dative-uses/dative-thing-possessed-disputed": {
        "display_name": "Dative of Thing Possessed (disputed)",
        "description": "who possesses"
      },
      "dative/pure-dative-uses/predicate-dative": {
        "display_name": "Predicate Dative",
        "description": "simple apposition in dative case made emphatic by participial form of the equative verb"
      },
      "dative/pure-dative-uses/dative-simple-apposition": {
        "display_name": "Dative in Simple Apposition",
        "description": "dative substantive adjacent to another dative substantive, referring to the same thing/person"
      }
    },
    "lexical_options": [
      "παιδίον",
      "δοῦλος",
      "γυνή"
    ]
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with an adverbial dependent clause: manner means, articular infinitive",
      "formation": "ἐν τῷ followed by an infinitive.",
      "function": "Says how the controlling verb's action was carried out. Render with 'by ... -ing'.",
      "syntactic_category": "Means - a syntactic usage, under Infinitive > Adverbial. Syntactic explanation: ἐν τῷ + infinitive; describes the way in which the action of the controlling verb is accomplished; translate by … doing, etc..",
      "position": "after the main clause by default; before it when you mean to give it emphasis",
      "paradigm": {
        "name": "Present Middle Infinitive",
        "forms": {
          "λύεσθαι (λύω, thematic)": {
            "present middle infinitive": "λύεσθαι"
          },
          "μένεσθαι (μένω, liquid)": {
            "present middle infinitive": "μένεσθαι"
          },
          "γεννᾶσθαι (γεννάω, contract -άω)": {
            "present middle infinitive": "γεννᾶσθαι"
          },
          "ποιεῖσθαι (ποιέω, contract -έω)": {
            "present middle infinitive": "ποιεῖσθαι"
          },
          "φανεροῦσθαι (φανερόω, contract -όω)": {
            "present middle infinitive": "φανεροῦσθαι"
          },
          "ἵστασθαι (ἵστημι, athematic)": {
            "present middle infinitive": "ἵστασθαι"
          },
          "τίθεσθαι (τίθημι, athematic)": {
            "present middle infinitive": "τίθεσθαι"
          },
          "δίδοσθαι (δίδωμι, athematic)": {
            "present middle infinitive": "δίδοσθαι"
          }
        }
      }
    },
    "also_include": [
      "Subjunctive in Indefinite Relative Clause - a syntactic usage, under Moods > Subjunctive > In Dependent (Subordinate) Clauses. Syntactic explanation: after ὅστις (ἄν/ἐάν) or ὅς (δʼ) ἄν; construction indicates a generic or indefinite subject; translate like an indicative (since the contingency is of the person, not the action)."
    ],
    "setting_options": {
      "s132": "A court clerk reads out a sentence of exile.",
      "s026": "A farmer's sons plant young olive trees that will not bear fruit for years."
    }
  }
}
```

### `accusative/substantival-uses-accusative/accusative-direct-object`

```json
{
  "item": {
    "item": {
      "key": "accusative/substantival-uses-accusative/accusative-direct-object",
      "display_name": "Accusative Direct Object",
      "description": "the immediate object of the action of a transitive verb"
    },
    "ancestors": [
      {
        "display_name": "Accusative",
        "description": "extent or limitation"
      },
      {
        "display_name": "Substantival Uses of the Accusative",
        "description": null
      }
    ],
    "sibling_usages": {
      "accusative/substantival-uses-accusative/double-accusatives": {
        "display_name": "Double Accusatives",
        "description": null
      },
      "accusative/substantival-uses-accusative/cognate-accusative-accusative-inner-object": {
        "display_name": "Cognate Accusative (Accusative of Inner Object)",
        "description": "direct object that shares lexically or conceptually the idea of the verb (“do not treasure treasures”)"
      },
      "accusative/substantival-uses-accusative/predicate-accusative": {
        "display_name": "Predicate Accusative",
        "description": "simple apposition made emphatic by a copula in participial form or infinitival form (an accusative related to subject of infinitive)"
      },
      "accusative/substantival-uses-accusative/accusative-subject-infinitive": {
        "display_name": "Accusative Subject of Infinitive",
        "description": "accusative of reference that functions like subject of infinitive (“I want you to know”)"
      },
      "accusative/substantival-uses-accusative/accusative-retained-object": {
        "display_name": "Accusative of Retained Object",
        "description": "the accusative of thing in a double accusative person-thing construction with an active verb retains its case when the verb is put in the passive (“I taught you the lesson” becomes “You were taught the lesson by me”)"
      },
      "accusative/substantival-uses-accusative/pendent-accusative-accusativum-pendens": {
        "display_name": "Pendent Accusative (Accusativum Pendens)",
        "description": "accusative thrown forward to the beginning of the clause, followed by a sentence in which it is replaced by a pronoun in the case required by the syntax—with reference to (subset of acc. of reference)"
      },
      "accusative/substantival-uses-accusative/accusative-simple-apposition": {
        "display_name": "Accusative in Simple Apposition",
        "description": "accusative substantive adjacent to another accusative substantive, referring to the same thing/person"
      }
    },
    "lexical_options": [
      "ἄρτος",
      "θύρα",
      "ἐπιστολή"
    ]
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with a relative clause: adjectival",
      "formation": "Relative pronoun agreeing with its antecedent in number and gender, its case set by its role inside the relative clause. It follows its referent.",
      "function": "Attributive only - it describes, explains or narrows the substantive it attaches to.",
      "syntactic_category": "Relative Pronouns - a syntactic usage, under Pronouns > Semantic Categories. Syntactic explanation: ὅς and ὅστις labeled relative pronouns because they relate to more than one clause.",
      "position": "after the main clause by default; before it when you mean to give it emphasis",
      "paradigm": {
        "name": "Relative Pronoun",
        "forms": {
          "ὅς": {
            "nominative masculine singular": "ὅς",
            "genitive masculine singular": "οὗ",
            "dative masculine singular": "ᾧ",
            "accusative masculine singular": "ὅν",
            "nominative masculine plural": "οἵ",
            "genitive masculine plural": "ὧν",
            "dative masculine plural": "οἷς",
            "accusative masculine plural": "οὕς"
          },
          "ἥ": {
            "nominative feminine singular": "ἥ",
            "genitive feminine singular": "ἧς",
            "dative feminine singular": "ῇ",
            "accusative feminine singular": "ἥν",
            "nominative feminine plural": "αἵ",
            "genitive feminine plural": "ὧν",
            "dative feminine plural": "αἷς",
            "accusative feminine plural": "ἅς"
          },
          "ὅ": {
            "nominative neuter singular": "ὅ",
            "genitive neuter singular": "οὗ",
            "dative neuter singular": "ᾧ",
            "accusative neuter singular": "ὅ",
            "nominative neuter plural": "ἅ",
            "genitive neuter plural": "ὧν",
            "dative neuter plural": "οἷς",
            "accusative neuter plural": "ἅ"
          }
        }
      }
    },
    "also_include": [],
    "setting_options": {
      "s129": "A craftsman carves a chair of state for a magistrate.",
      "s081": "A merchant swears by God that his cloth is the finest in the city."
    }
  }
}
```

### `article/regular-uses-article/as-pronoun-partially-independent-use/personal-pronoun`

```json
{
  "item": {
    "item": {
      "key": "article/regular-uses-article/as-pronoun-partially-independent-use/personal-pronoun",
      "display_name": "Personal Pronoun",
      "description": "functions as third person pronoun in nominative in μὲν … δέ construction or with δέ alone"
    },
    "ancestors": [
      {
        "display_name": "The Article",
        "description": "basically a conceptualizer & identifier, not a definitizer"
      },
      {
        "display_name": "Regular Uses of the Article",
        "description": null
      },
      {
        "display_name": "As a Pronoun ([partially] Independent Use)",
        "description": null
      }
    ],
    "sibling_usages": {
      "article/regular-uses-article/as-pronoun-partially-independent-use/relative-pronoun": {
        "display_name": "Relative Pronoun",
        "description": "who is, which is (the article with second and third attributive positions in which the modifier is not an adjective)"
      },
      "article/regular-uses-article/as-pronoun-partially-independent-use/possessive-pronoun": {
        "display_name": "Possessive Pronoun",
        "description": "his, her (used in contexts in which possession is implied)"
      }
    },
    "lexical_options": [
      "μαθητής",
      "ὄχλος",
      "στρατιώτης"
    ]
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a single main clause",
      "formation": "A single independent clause: nominative subject, finite verb, and an accusative direct object if the verb is transitive.",
      "function": "One unsubordinated assertion. Unmarked order is subject, then predicate, then complement."
    },
    "also_include": [
      "Dative of Association/Accompaniment - a syntactic usage, under Dative > Instrumental Dative Uses. Syntactic explanation: the person or thing one associates with or accompanies—in association with."
    ],
    "setting_options": {
      "s013": "An old teacher tests his pupils on the letters they copied onto wax tablets.",
      "s068": "Two apprentices race to finish a table before their master returns."
    }
  }
}
```

### `voice/active/simple-active`

```json
{
  "item": {
    "item": {
      "key": "voice/active/simple-active",
      "display_name": "Simple Active",
      "description": "subject performs or experiences the action"
    },
    "ancestors": [
      {
        "display_name": "Voice",
        "description": "indicates how subject is related to the action [or state] expressed by the verb"
      },
      {
        "display_name": "Active",
        "description": "Subject performs, produces, or experiences the action or exists in the state expressed by the verb"
      }
    ],
    "sibling_usages": {
      "voice/active/causative-active-k-ergative": {
        "display_name": "Causative Active (a.k.a. Ergative)",
        "description": "subject is not directly involved in the action, but is the ultimate source of it"
      },
      "voice/active/stative-active": {
        "display_name": "Stative Active",
        "description": "subject exists in the state indicated by the verb"
      },
      "voice/active/reflexive-active": {
        "display_name": "Reflexive Active",
        "description": "active verb + reflexive pronoun (subject acts upon himself or herself)"
      }
    },
    "lexical_options": [
      "γράφω",
      "διώκω",
      "θεραπεύω"
    ]
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with a relative clause: adjectival",
      "formation": "Relative pronoun agreeing with its antecedent in number and gender, its case set by its role inside the relative clause. It follows its referent.",
      "function": "Attributive only - it describes, explains or narrows the substantive it attaches to.",
      "syntactic_category": "Relative Pronouns - a syntactic usage, under Pronouns > Semantic Categories. Syntactic explanation: ὅς and ὅστις labeled relative pronouns because they relate to more than one clause.",
      "position": "after the main clause by default; before it when you mean to give it emphasis",
      "paradigm": {
        "name": "Relative Pronoun",
        "forms": {
          "ὅς": {
            "nominative masculine singular": "ὅς",
            "genitive masculine singular": "οὗ",
            "dative masculine singular": "ᾧ",
            "accusative masculine singular": "ὅν",
            "nominative masculine plural": "οἵ",
            "genitive masculine plural": "ὧν",
            "dative masculine plural": "οἷς",
            "accusative masculine plural": "οὕς"
          },
          "ἥ": {
            "nominative feminine singular": "ἥ",
            "genitive feminine singular": "ἧς",
            "dative feminine singular": "ῇ",
            "accusative feminine singular": "ἥν",
            "nominative feminine plural": "αἵ",
            "genitive feminine plural": "ὧν",
            "dative feminine plural": "αἷς",
            "accusative feminine plural": "ἅς"
          },
          "ὅ": {
            "nominative neuter singular": "ὅ",
            "genitive neuter singular": "οὗ",
            "dative neuter singular": "ᾧ",
            "accusative neuter singular": "ὅ",
            "nominative neuter plural": "ἅ",
            "genitive neuter plural": "ὧν",
            "dative neuter plural": "οἷς",
            "accusative neuter plural": "ἅ"
          }
        }
      }
    },
    "also_include": [],
    "setting_options": {
      "s036": "Two merchants swear an oath over a disputed shipment of wool.",
      "s019": "A girl hides her brother's broken toy from their father."
    }
  }
}
```

### `moods/indicative/declarative-indicative`

```json
{
  "item": {
    "item": {
      "key": "moods/indicative/declarative-indicative",
      "display_name": "Declarative Indicative",
      "description": "presents assertion as a noncontingent (or unqualified) statement"
    },
    "ancestors": [
      {
        "display_name": "Moods",
        "description": "present [the speaker’s portrayal of his affirmation of certainty of] the verbal action or state with reference to its actuality or potentiality"
      },
      {
        "display_name": "Indicative",
        "description": "The mood of assertion, or presentation of certainty"
      }
    ],
    "sibling_usages": {
      "moods/indicative/interrogative-indicative": {
        "display_name": "Interrogative Indicative",
        "description": "question of fact; expects a declarative indicative in response"
      },
      "moods/indicative/conditional-indicative": {
        "display_name": "Conditional Indicative",
        "description": "indicative with εἰ in protasis—first class: assumed true for sake of argument; second class: assumed false (for sake of argument)"
      },
      "moods/indicative/potential-indicative": {
        "display_name": "Potential Indicative",
        "description": "semantically equivalent to a potential mood, due to verbal root; found in verbs of obligation, wish, or desire (such as ὀφείλω, δεῖ, θέλω), followed by infinitive"
      },
      "moods/indicative/cohortative-command-volitive-indicative": {
        "display_name": "Cohortative (Command, Volitive) Indicative",
        "description": "future indicative is sometimes used for a command"
      },
      "moods/indicative/indicative-ὃτι": {
        "display_name": "The Indicative with Ὃτι",
        "description": null
      }
    },
    "lexical_options": [
      "βλέπω",
      "ἀκούω",
      "μένω"
    ]
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with an adverbial dependent clause: conditional, first class",
      "formation": "Protasis: εἰ plus the indicative, in any tense. Apodosis: any mood or tense.",
      "function": "The speaker takes the condition as true so the argument can proceed from it, and the apodosis then follows naturally. This is not the same as 'since', and it is not a bare logical connection - the protasis may in fact be false and still be granted for the sake of the argument.",
      "syntactic_category": "First Class Condition - a syntactic usage, under Conditional Sentences > II. Conditional Sentences in Greek (especially the NT). Syntactic explanation: the assumption of truth for the sake of argument (does not mean since, nor is it a simple, logical condition); protasis: εἰ + indicative (in any tense)/apodosis: any mood, any tense (689, 690–94).",
      "position": "before the main clause by default; after it when you mean to give it emphasis"
    },
    "also_include": [
      "Temporal - a syntactic usage, under Conjunctions > Adverbial Functions. Syntactic explanation: translations vary (indicates the time of the action); ἄχρι, ἕως, ὅταν, ὅτε, οὐδέποτε (negative temporal), οὐκέτι (negative temporal), οὔπω (negative temporal), ποτέ, and ὡς."
    ],
    "setting_options": {
      "s094": "A shipowner hires sailors for one last voyage before the winter storms.",
      "s192": "A father learns that the gold ring he bought is genuine after all."
    }
  }
}
```

### `tense/present/instantaneous-present-k-aoristic-punctiliar-present`

```json
{
  "item": {
    "item": {
      "key": "tense/present/instantaneous-present-k-aoristic-punctiliar-present",
      "display_name": "Instantaneous Present (a.k.a. Aoristic or Punctiliar Present)",
      "description": "action occurs at the moment of speaking; usually a performative statement (e.g., “I tell you the truth, the Rams won the game”); indicative only"
    },
    "ancestors": [
      {
        "display_name": "Tense",
        "description": "indicates the speaker’s presentation of the verbal action [or state] with reference to its aspect and, under certain conditions, its time"
      },
      {
        "display_name": "Present",
        "description": "Portrays the action as an internal or progressive event, without regard for beginning or end; in indicative, present time (generally)"
      }
    ],
    "sibling_usages": {
      "tense/present/narrow-band-presents": {
        "display_name": "Narrow-Band Presents",
        "description": null
      },
      "tense/present/progressive-present-k-descriptive-present": {
        "display_name": "Progressive Present (a.k.a. Descriptive Present)",
        "description": "at this present time, right now (describes a scene in progress, esp. in narrative literature)"
      },
      "tense/present/broad-band-presents": {
        "display_name": "Broad-Band Presents",
        "description": null
      }
    },
    "lexical_options": [
      "λέγω",
      "παρακαλέω",
      "ἀσπάζομαι"
    ]
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with an adverbial dependent clause: time, articular infinitive",
      "formation": "μετὰ τό plus infinitive for action before the main verb; ἐν τῷ plus infinitive for action alongside it; πρὸ τοῦ, πρίν or πρὶν ἤ plus infinitive for action after it.",
      "function": "Places the main verb's action in time. Render with 'after', 'while / as / when', or 'before' plus a finite verb, according to the preposition used.",
      "syntactic_category": "Time - a syntactic usage, under Infinitive > Adverbial.",
      "paradigm": {
        "name": "First Aorist Active Infinitive",
        "forms": {
          "λῦσαι (λύω, thematic)": {
            "aorist active infinitive": "λῦσαι"
          },
          "μεῖναι (μένω, liquid)": {
            "aorist active infinitive": "μεῖναι"
          },
          "γεννῆσαι (γεννάω, contract -άω)": {
            "aorist active infinitive": "γεννῆσαι"
          },
          "ποιῆσαι (ποιέω, contract -έω)": {
            "aorist active infinitive": "ποιῆσαι"
          },
          "φανερῶσαι (φανερόω, contract -όω)": {
            "aorist active infinitive": "φανερῶσαι"
          },
          "στῆσαι (ἵστημι, first aorist)": {
            "aorist active infinitive": "στῆσαι"
          }
        }
      }
    },
    "also_include": [],
    "setting_options": {
      "s162": "Two neighbours argue over whether one may draw water from the other's cistern.",
      "s202": "A workman's excuse for his absence proves to be empty."
    }
  }
}
```

### `participle/substantival-independent`

```json
{
  "item": {
    "item": {
      "key": "participle/substantival-independent",
      "display_name": "Substantival (Independent)",
      "description": "the one who, the thing which; functions in the place of a substantive; can perform virtually any function a noun can; verbal aspect usually retained"
    },
    "ancestors": [
      {
        "display_name": "Participle",
        "description": "declinable verbal adjective"
      }
    ],
    "sibling_usages": {
      "participle/adjectival-participles": {
        "display_name": "Adjectival Participles",
        "description": "adjectival nature is emphasized over verbal; if the participle is articular, it must be adjectival; if anarthrous, it may be adjectival"
      },
      "participle/adjectival-proper-dependent": {
        "display_name": "Adjectival Proper (Dependent)",
        "description": null
      },
      "participle/verbal-participles": {
        "display_name": "Verbal Participles",
        "description": "verbal nature is emphasized over adjectival; only with anarthrous participles, usually nominative and dependent on main verb"
      },
      "participle/finite-verb-εἰμί": {
        "display_name": "Finite Verb (of εἰμί)",
        "description": "+"
      },
      "participle/participle": {
        "display_name": "Participle",
        "description": "="
      },
      "participle/present": {
        "display_name": "Present",
        "description": "+"
      },
      "participle/present-2": {
        "display_name": "Present",
        "description": "="
      },
      "participle/imperfect": {
        "display_name": "Imperfect",
        "description": "+"
      },
      "participle/present-4": {
        "display_name": "Present",
        "description": "="
      },
      "participle/future": {
        "display_name": "Future",
        "description": "+"
      },
      "participle/present-5": {
        "display_name": "Present",
        "description": "="
      },
      "participle/present-6": {
        "display_name": "Present",
        "description": "+"
      },
      "participle/perfect": {
        "display_name": "Perfect",
        "description": "="
      },
      "participle/imperfect-3": {
        "display_name": "Imperfect",
        "description": "+"
      },
      "participle/perfect-3": {
        "display_name": "Perfect",
        "description": "="
      },
      "participle/pluperfect": {
        "display_name": "Pluperfect",
        "description": null
      }
    },
    "lexical_options": [
      "πιστεύω",
      "ἀκολουθέω",
      "ἐργάζομαι"
    ]
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a single main clause",
      "formation": "A single independent clause: nominative subject, finite verb, and an accusative direct object if the verb is transitive.",
      "function": "One unsubordinated assertion. Unmarked order is subject, then predicate, then complement."
    },
    "also_include": [
      "With a Pronominal Adjective - a syntactic usage, under The Article > Absence of the Article > Definite. Syntactic explanation: nouns with πᾶς, ὅλος, etc. do not need the article to be definite, for either the class as a whole (“all”) or distributively (“every”) is being specified."
    ],
    "setting_options": {
      "s188": "A goatherd milks his goats at dawn.",
      "s048": "A steward counts the household stores before winter and finds the oil jars half empty."
    }
  }
}
```

### `conjunctions/ascensive`

```json
{
  "item": {
    "item": {
      "key": "conjunctions/ascensive",
      "display_name": "Ascensive",
      "description": "even (final addition or point of focus); καί, δέ, and μηδέ"
    },
    "ancestors": [
      {
        "display_name": "Conjunctions",
        "description": null
      }
    ],
    "sibling_usages": {
      "conjunctions/logical-functions": {
        "display_name": "Logical Functions",
        "description": "relate the movement of thought from one passage to another by expressing logical relationships"
      },
      "conjunctions/connective-continuative-coordinate": {
        "display_name": "Connective (continuative, coordinate)",
        "description": "and, also (if emphatic [adjunctive]); (connects an additional element to a discussion); καί and δέ"
      },
      "conjunctions/contrastive-adversative": {
        "display_name": "Contrastive (adversative)",
        "description": "but, rather, however (contrast or opposing thought to the idea to which it is connected); ἀλλά, πλήν, sometimes καί and δέ"
      },
      "conjunctions/correlative": {
        "display_name": "Correlative",
        "description": "paired conjunctions expressing various relationships; e.g., μέν … δέ (on the one hand … on the other hand); καί … καί (both … and)"
      },
      "conjunctions/disjunctive-alternative": {
        "display_name": "Disjunctive (Alternative)",
        "description": "or (suggests an alternative possibility to the idea to which it is connected); ἤ"
      },
      "conjunctions/emphatic": {
        "display_name": "Emphatic",
        "description": "certainly, indeed (involves intensifying the normal sense of a conjunction); ἀλλά (certainly), οὐ μή (certainly not or by no means), οὖν (certainly); true emphatic conjunctions include γε, δή, μενοῦνγε, μέντοι, ναί, and νή"
      },
      "conjunctions/explanatory": {
        "display_name": "Explanatory",
        "description": "for, you see, or that is, namely (conjunction indicates additional information being given to what has been described); γάρ, δέ, εἰ (after verbs of emotion), and καί"
      },
      "conjunctions/inferential": {
        "display_name": "Inferential",
        "description": "therefore (gives a deduction, conclusion, or summary to the preceding discussion); ἄρα, γάρ, διό, διότι, οὖν, πλήν, τοιγαροῦν, τοινῦν, and ὥστε."
      },
      "conjunctions/transitional": {
        "display_name": "Transitional",
        "description": "now, then (involves the change to a new topic of discussion, especially in narrative); οὖν and especially δέ"
      },
      "conjunctions/adverbial-functions": {
        "display_name": "Adverbial Functions",
        "description": "amplify the verbal idea in a specific way (usually subordinate conjunctions)"
      }
    },
    "lexical_options": [
      "τελώνης",
      "παιδίον",
      "πτωχός"
    ]
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with an adverbial dependent clause: concessive, adverbial participle",
      "formation": "Anarthrous participle matching its subject in case, number and gender.",
      "function": "Concedes something: the main verb holds true in spite of what the participle describes. Render with 'although'.",
      "syntactic_category": "Concession - a syntactic usage, under Participle > Verbal Participles > Dependent Verbal Participles > Adverbial (or Circumstantial). Syntactic explanation: although (implies that the state or action of the main verb is true in spite of the state or action of the participle).",
      "position": "after the main clause by default; before it when you mean to give it emphasis",
      "paradigm": {
        "name": "Present Active Participle",
        "forms": {
          "λύων (λύω, thematic)": {
            "present active participle nominative masculine singular": "λύων",
            "present active participle genitive masculine singular": "λύοντος",
            "present active participle dative masculine singular": "λύοντι",
            "present active participle accusative masculine singular": "λύοντα",
            "present active participle nominative masculine plural": "λύοντες",
            "present active participle genitive masculine plural": "λυόντων",
            "present active participle dative masculine plural": "λύουσι(ν)",
            "present active participle accusative masculine plural": "λύοντας"
          },
          "λύουσα (λύω, thematic)": {
            "present active participle nominative feminine singular": "λύουσα",
            "present active participle genitive feminine singular": "λυούσης",
            "present active participle dative feminine singular": "λυούσῃ",
            "present active participle accusative feminine singular": "λύουσαν",
            "present active participle nominative feminine plural": "λύουσαι",
            "present active participle genitive feminine plural": "λυουσῶν",
            "present active participle dative feminine plural": "λυούσαις",
            "present active participle accusative feminine plural": "λυούσας"
          },
          "λῦον (λύω, thematic)": {
            "present active participle nominative neuter singular": "λῦον",
            "present active participle genitive neuter singular": "λύοντος",
            "present active participle dative neuter singular": "λύοντι",
            "present active participle accusative neuter singular": "λῦον",
            "present active participle nominative neuter plural": "λύοντα",
            "present active participle genitive neuter plural": "λυόντων",
            "present active participle dative neuter plural": "λύουσι(ν)",
            "present active participle accusative neuter plural": "λύοντα"
          },
          "ἱστάς (ἵστημι, athematic)": {
            "present active participle nominative masculine singular": "ἱστάς",
            "present active participle genitive masculine singular": "ἱστάντος"
          },
          "ἱστᾶσα (ἵστημι, athematic)": {
            "present active participle nominative feminine singular": "ἱστᾶσα",
            "present active participle genitive feminine singular": "ἱστάσης"
          },
          "ἱστάν (ἵστημι, athematic)": {
            "present active participle nominative neuter singular": "ἱστάν",
            "present active participle genitive neuter singular": "ἱστάντος"
          },
          "τιθείς (τίθημι, athematic)": {
            "present active participle nominative masculine singular": "τιθείς",
            "present active participle genitive masculine singular": "τιθέντος"
          },
          "τιθεῖσα (τίθημι, athematic)": {
            "present active participle nominative feminine singular": "τιθεῖσα",
            "present active participle genitive feminine singular": "τιθείσης"
          },
          "τιθέν (τίθημι, athematic)": {
            "present active participle nominative neuter singular": "τιθέν",
            "present active participle genitive neuter singular": "τιθέντος"
          },
          "διδούς (δίδωμι, athematic)": {
            "present active participle nominative masculine singular": "διδούς",
            "present active participle genitive masculine singular": "διδόντος"
          },
          "διδοῦσα (δίδωμι, athematic)": {
            "present active participle nominative feminine singular": "διδοῦσα",
            "present active participle genitive feminine singular": "διδούσης"
          },
          "διδόν (δίδωμι, athematic)": {
            "present active participle nominative neuter singular": "διδόν",
            "present active participle genitive neuter singular": "διδόντος"
          },
          "δεικνύς (δείκνυμι, athematic)": {
            "present active participle nominative masculine singular": "δεικνύς",
            "present active participle genitive masculine singular": "δεικνύντος"
          },
          "δεικνῦσα (δείκνυμι, athematic)": {
            "present active participle nominative feminine singular": "δεικνῦσα",
            "present active participle genitive feminine singular": "δεικνύσης"
          },
          "δεικνύν (δείκνυμι, athematic)": {
            "present active participle nominative neuter singular": "δεικνύν",
            "present active participle genitive neuter singular": "δεικνύντος"
          }
        }
      }
    },
    "also_include": [],
    "setting_options": {
      "s169": "A traveller must wait in a town until the bridge is repaired.",
      "s093": "Debtors in a crowded cell share a single blanket through a cold night."
    }
  }
}
```

### `conditional-sentences/ii-conditional-sentences-greek-especially-nt/first-class-condition`

```json
{
  "item": {
    "item": {
      "key": "conditional-sentences/ii-conditional-sentences-greek-especially-nt/first-class-condition",
      "display_name": "First Class Condition",
      "description": "the assumption of truth for the sake of argument (does not mean since, nor is it a simple, logical condition); protasis: εἰ + indicative (in any tense)/apodosis: any mood, any tense (689, 690–94)"
    },
    "ancestors": [
      {
        "display_name": "Conditional Sentences",
        "description": null
      },
      {
        "display_name": "II. Conditional Sentences in Greek (especially the NT)",
        "description": null
      }
    ],
    "sibling_usages": {
      "conditional-sentences/ii-conditional-sentences-greek-especially-nt/second-class-condition": {
        "display_name": "Second Class Condition",
        "description": "the assumption of an untruth (for the sake of argument); protasis: εἰ + indicative of secondary tense (aorist or imperfect usually)/apodosis: ἄν (usually) + secondary tense in indicative (689, 694–96)"
      },
      "conditional-sentences/ii-conditional-sentences-greek-especially-nt/third-class-condition": {
        "display_name": "Third Class Condition",
        "description": "range of nuances: (a) a logical connection (if A, then B) in the present time (present general condition or fifth class condition), (b) hypothetical situation, and (c) more probable future occurrence; ἐάν + subjunctive, any tense; apodosis: any tense, any mood (present indicative for present general condition) (689, 696–99)"
      },
      "conditional-sentences/ii-conditional-sentences-greek-especially-nt/fourth-class-condition-less-probable-future": {
        "display_name": "Fourth Class Condition (Less Probable Future)",
        "description": "possible condition in the future, usually remote possibility (such as if he could do something, if perhaps this should occur); protasis: εἰ + optative; apodosis: optative + ἄν (689, 699–701)"
      }
    },
    "lexical_options": [
      "υἱός",
      "ἔργον",
      "ἀληθής"
    ]
  },
  "recent_generations": [],
  "student": {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable"
  },
  "sentence_plan": {
    "sentence_shape": {
      "shape": "a main clause with a relative clause: adjectival",
      "formation": "Relative pronoun agreeing with its antecedent in number and gender, its case set by its role inside the relative clause. It follows its referent.",
      "function": "Attributive only - it describes, explains or narrows the substantive it attaches to.",
      "syntactic_category": "Relative Pronouns - a syntactic usage, under Pronouns > Semantic Categories. Syntactic explanation: ὅς and ὅστις labeled relative pronouns because they relate to more than one clause.",
      "position": "after the main clause by default; before it when you mean to give it emphasis",
      "paradigm": {
        "name": "Relative Pronoun",
        "forms": {
          "ὅς": {
            "nominative masculine singular": "ὅς",
            "genitive masculine singular": "οὗ",
            "dative masculine singular": "ᾧ",
            "accusative masculine singular": "ὅν",
            "nominative masculine plural": "οἵ",
            "genitive masculine plural": "ὧν",
            "dative masculine plural": "οἷς",
            "accusative masculine plural": "οὕς"
          },
          "ἥ": {
            "nominative feminine singular": "ἥ",
            "genitive feminine singular": "ἧς",
            "dative feminine singular": "ῇ",
            "accusative feminine singular": "ἥν",
            "nominative feminine plural": "αἵ",
            "genitive feminine plural": "ὧν",
            "dative feminine plural": "αἷς",
            "accusative feminine plural": "ἅς"
          },
          "ὅ": {
            "nominative neuter singular": "ὅ",
            "genitive neuter singular": "οὗ",
            "dative neuter singular": "ᾧ",
            "accusative neuter singular": "ὅ",
            "nominative neuter plural": "ἅ",
            "genitive neuter plural": "ὧν",
            "dative neuter plural": "οἷς",
            "accusative neuter plural": "ἅ"
          }
        }
      }
    },
    "also_include": [
      "Possessive Pronoun - a syntactic usage, under The Article > Regular Uses of the Article > As a Pronoun ([partially] Independent Use). Syntactic explanation: his, her (used in contexts in which possession is implied)."
    ],
    "setting_options": {
      "s092": "A household guard is bribed to leave a gate unbarred.",
      "s027": "Neighbours put out a kitchen fire before it spreads to the roof."
    }
  }
}
```

## System prompt (vocabulary)

```
 You are an expert Koine Greek linguist and a specialized language-learning content developer. You build single spaced-repetition cards for a student working through a structured Koine Greek curriculum. You are building ONE card. You are not teaching, not explaining at length, and not producing an exercise set. Everything you write will be seen by a student in a few seconds of review.

  HARD CONSTRAINTS (apply to every card; per-type rules add to these, never override them):
  1. TOTAL KOINE FIDELITY — every Greek word, form, and construction must be correct for the Koine/Biblical period; no Classical/Attic or Modern Greek mixing; preserve all diacritics and inflections precisely; accent and breathing are part of the answer.
  2. ATOMIC SCOPE — exactly one retrieval demand per card; keep surrounding vocabulary/syntax intuitive so cognitive load stays primarily on the target item; one concept per card.
  3. VOCABULARY WITHIN REASONABLE STUDENT SCOPE — every non-target word must be vocabulary the student has likely already learned. You maybe be given a list of student vocabulary, or you may not. You will, however, be given a student's general level and must utilize your knowledge of NT vocabulary frequency to guage if your sentence is likely known based on student level. Your sentence is checked against the list after you write it: one or two words outside it are allowed and are glossed for the student on the card, but a sentence that needs more than that is thrown out and regenerated. Within that bound, use the full range available to you. As the student's vocabulary grows the sentences should grow with it — do not default to the plainest possible words at higher levels. A card built from bare elementary vocabulary is a boring card and teaches less than it could, so be reasonable but do not play too safe.
  4. RESPECT THE CURRICULUM BOUNDARY — you are given both the morphological category rules the student HAS covered and those they have NOT. Use only what has been covered, even if an uncovered form would improve the sentence. The uncovered list is there so you know what to avoid, not as a menu.
  5. NATURAL CONTEXT — the sentence must be semantically coherent, idiomatic Koine, and illustrate the target's meaning naturally. Idiom includes word order: build the unmarked order set out under WORD ORDER below, and depart from it only for an emphasis you intend.
  6. VARIABILITY, SUBORDINATED — vary lexical choice, sentence shape, and grammatical texture across cards, but always secondary to fidelity and atomic scope.
  7. DIFFICULTY MATCHES LEVEL — you are supplied with the current level of the student - beginner: predictable, simple sentence form, first-semester vocabulary; beyond_beginner: vary cases, tenses, moods, participles, prepositional phrases, relative clauses, conjunctions, word order — only within what constraint 4 permits; advanced: You have free reign of creative formulation under the restrictions of the restraints.
  8. RECORD THE DECISIONS — work through the REFLECTION below before composing, then set out the choices behind the finished card in "reasoning": 1-4 short sentences of compressed analysis ending in a decision. This is an editorial note about the card, of the kind a writer leaves for the editor who will check it — what the item's sense rests on, which competing reading the clause shuts out, and why this scene and not another. It is read by the auditor, never shown to the student, and never skipped.
  9. THE GLOSS IS CONTEXTUAL AND SHORT — where a gloss is requested (not always applicable), 1-5 words, rendering the target as used in this sentence, not simply the glossary default.
  10. NO NEW OR CONTROVERSIAL DOCTRINE — keep sentences theologically unobjectionable and small in scope; nothing sexual, gratuitously violent, politically inflammatory, or otherwise unsuitable for a study card.
  11. BUILD ON THE REFERENCE, DO NOT REPEAT IT — in the case you are given one or more hand-vetted reference cards for this item, those set the standard for quality, register, and constraint compliance; match it. Do not reuse its scene, its vocabulary choices, or its sentence shape, and do not paraphrase or template-swap any recent generation. Write something genuinely different within the same constraints, utilizing it only as an example of a premium generation.
  12. FIDELITY ABOVE FLUENCY — where given data conflicts with your own recollection of Greek, follow the data; the rule's stated formation, the paradigm's forms, and the student's vocabulary list are authoritative: they are drawn from cited scholarly reference works and take precedence over recollection.
  13. NO RECOGNISABLE TEXT — do not reproduce or lightly reword a passage of the Greek New Testament or the Septuagint. Its people, places, objects and ideas are all yours to use; its wording is not. This is not a matter of taste. A student who recognises the line recalls the line instead of retrieving the item, and the card goes on looking correct while testing nothing. Write the world of the New Testament, not the verses.

  ECHO CRITERIA — constraint 13 is checked by a separate auditor after you write. Read what is actually being tested before the four axes, because the usual mistake is to check the wrong thing.

  THE SETTING IS GIVEN; THE WORDING IS YOURS. The world these cards live in is the world the New Testament was written in — its trades, households, roads, markets, festivals and law — and you are handed two everyday situations from it in "sentence_plan". Build the scene inside one of them. They are chosen for you because a word's first pull is toward the passage it is famous for — βαπτίζω toward the Jordan, κράζω toward the blind man by the road — and once the scene is that passage, its wording follows. So do not steer a setting back toward a known episode or parable, and use no New Testament figure by name. The item must still be at home in the scene you write: a card for βαπτίζω needs an immersion, a card for ποιμήν a flock. Put the word to its ordinary work inside the setting you chose.
  Within that, write fresh Koine: your clauses, your arrangement, your choice of what stands beside what. A short run held in common with a verse is unavoidable and fine — one such piece at most. What fails is a sentence assembled out of a particular passage's actual wording, however the scene around it has been redressed. The question is never "is this biblical" but always "are these its words".
  1. WORDING — does any run of words, any clause, any phrase reproduce a passage verbatim or nearly so? Changing a preposition, a case, or the word order does not make a borrowed line your own. This is the criterion. The three below exist only because wording can be lifted in ways a plain string comparison misses.
  2. STRUCTURE — have you rebuilt one verse's clause architecture and swapped its vocabulary out, so the sentence is that verse in other clothes? Writing about something the corpus also describes is fine; reproducing the sequence of constructions a specific passage used is not.
  3. SCENE — has the setting you were given drifted into an episode the corpus depicts, your clauses tracking its beats? The setting exists to keep the card out of that. Stay in it, and write a moment that belongs to it: its own participants, its own point in the action, details no passage gives.
  4. REGISTER — have you reached for a formula that is itself a piece of the text? ἀμὴν λέγω ὑμῖν, ἐγένετο δὲ ἐν τῷ, μακάριοι οἱ, οὐαὶ ὑμῖν, χάρις ὑμῖν καὶ εἰρήνη. Those are quotations wherever they appear, and they are the first frames to hand, which is exactly why they are the wrong ones.

  THEOLOGICAL RENDERING — separate from the four above and judged on its own. Where the item requires a theological term, use it and render it in a way that is contextually appropriate and doctrinally uncontentious. The vocabulary is never the problem. What is checked is the claim built out of it: an ordinary, unremarkable use is what you want; a novel, disputable or misleading one fails however good the Greek. This is constraint 10 applied to the lexicon.

WORD ORDER IN NEW TESTAMENT GREEK

Greek word order is flexible but not free, and it carries meaning. The normal ("unmarked")
pattern is invisible to a reader; a departure from it ("marked") signals prominence. Build the
unmarked pattern unless you intend the emphasis - and if you do, know which emphasis you intend.


1. HARD CONSTRAINTS - never a choice. Violating these produces non-Greek.

- The article immediately precedes its substantive: ὁ δοῦλος, never δοῦλος ὁ.
- A preposition precedes its object (χάριν, χωρίς, ἕνεκα are the rare exceptions).
- Relative and interrogative words open their clause, whatever their grammatical function
  inside it - subject, object and indirect object alike.
- Postpositive words never open a clause: ἄν, γάρ, δέ, γέ, μέν, οὖν, the enclitics ποτέ, πώς,
  τέ, and the pronouns με, μου, μοι. Put them second - but "second" is a range, not a point:
  anywhere from directly after the first word (ἐν δὲ τῷ ἀγρῷ) to just past the first complete
  phrase (ὁ ἀγρὸς γὰρ ὁ τοῦ πατρός).
- These never close a clause: ἀλλά, ἤ, καί, οὐδέ/μηδέ, οὔτε/μήτε, εἴτε, μή ("lest"), relative
  pronouns, εἰ, ἐπεί, ἵνα, ὁ, and most prepositions.
- These tend to sit near the front: interrogatives, clause negatives, words of succession
  (πρῶτον, ἔπειτα, εἶτα), most pronouns including nominative demonstratives, νῦν, τότε, αὐτός,
  ἄλλος, ἕτερος, ἀμφότεροι, πολύς, πολλάκις, εἷς.


2. UNMARKED CLAUSE ORDER

The predicate is the minimal unit of a Greek clause - a clause may consist of nothing else. Do
not treat subject-verb-object as a required frame when reading.

When subject, predicate and complement are all expressed, the unmarked order is:

    SUBJECT - PREDICATE - COMPLEMENT

The complement may fall on either side of the predicate in roughly equal proportion, with a
slight preference for following it. An expressed subject placed first is doing work: it marks
the topic, or marks a shift to a new one. That force weakens as the subject moves rightward.

One documented exception: in clauses with an imperative, the predicate is fronted.


3. DEPENDENT CLAUSE POSITION

A dependent clause goes before or after the main clause; it rarely interrupts it. Which side is
fixed by the clause's MEANING, not by how it is built - a conditional participle precedes and a
result participle follows, exactly as the matching conjunction would.

BEFORE the main clause:
    conditional          εἰ, ἐάν
    temporal "when"      ὅτε, ὅταν

AFTER the main clause:
    purpose              ἵνα, ὅπως
    result               ἵνα
    cause                ὅτι, ἐπεί, γάρ
    content / complement ἵνα, ὅτι
    temporal "until"     ἕως, ἄχρι
    local                ὅπου
    comparative          καθώς, ὡς
    concessive           εἰ καί, καίπερ
    relative             follows its referent (93% in Paul, 96% in Luke)

Moving a clause to the opposite side is the marking device: it signals prominence. A relative
clause serving as an object, for instance, can be placed before its verb for that reason.

A subject or object that is itself a clause moves to the rear of the main clause, behind the
single words and phrases. That is normal and carries no emphasis.


4. MARKING

Practically all marking is FRONTING: moving an element, usually a nominal, forward - usually
before the verb. Front an element only for one of these reasons:

    Contrast          front BOTH contrasted elements, each before its own verb
    Contraexpectation front the element that defeats the expectation
    Comparison        front both compared elements, each before its own verb
    Topicalization    front a newly introduced topic
    Motif             front the first mention of a recurring motif; often accusative
    Rhetorical        front the element carrying the speaker's emotion or expectation

These movements are NOT emphatic. Treat them as normal and do not read prominence into them:
    - a pronoun subject moves before the verb
    - a pronoun object sits immediately after the verb (direct object before indirect)
    - a clause-shaped subject or object moves to the rear
    - a negative stands immediately before the verb

Negative placement changes meaning: a negative immediately before the verb negates the whole
clause, while a negative before some other element negates only that element and pulls it
forward.

Orders that are possibly emphatic once produced:
    direct object before verb                   τὸν ἀγρὸν ἐπώλησεν
    subject before verb                         ὁ γεωργὸς ἐπώλησεν τὸν ἀγρόν
    predicate nominative before subject or verb τέκτων ἦν ὁ ἀνήρ
    genitive modifier before its noun           τοῦ πατρὸς τὸν ἀγρὸν ἠγόρασεν
    subject or object before an imperative      τὸ ἱμάτιον δὸς τῷ δούλῳ
    prepositional phrase before verb            ἐν τῇ ἀγορᾷ ἠγόρασεν ἰχθύας
    indirect object before verb                 τῷ δούλῳ ἔδωκεν τὸ ἱμάτιον


5. ORDER INSIDE A PHRASE - tendencies, and author-dependent

Do not treat these as rules. The adjective in particular splits by author, in opposite
directions:

    genitive modifier    follows its noun     96% Paul, 99% Luke    ὁ ἀγρὸς τοῦ πατρός
    demonstrative        follows its noun     85% Paul, 78% Luke    τὸ πλοῖον ἐκεῖνο
    adjective            FOLLOWS its noun     ~75% Luke and Mark    οἰκίαν μεγάλην
                         PRECEDES its noun    ~65% Paul             τοῖς πιστοῖς δούλοις

Where several modifiers stack, the sequence runs:
    head noun - demonstrative - indefinite - numeral - descriptive - participle

An adverb phrase rarely comes between a verb and its object; put it on one side or the other.

  REFLECTION — work through this before composing. It is where a card stops being merely correct and starts being worth studying.

  First, is the card sound?
    Where does this item's sense actually live? A concrete noun is recovered from what is done with it, or from what its absence costs; an abstract noun from the contrast it stands against; a verb from its object and its outcome; an inflected form from the absence of any competing parse. Find that anchor before you look for a scene — it tells you what the scene has to contain.
    What is the one competing reading a student could land on instead, and does your clause shut it out?
    Of the words this student knows, which earn their place here? The question is not which are permitted. A scene assembled from the twenty commonest words is a scene nobody remembers.
    Is there exactly one thing being retrieved?
    Does your English translation hand the answer over?

  Then, is the card worth meeting?
    THE SWAP TEST — could another word of the same class stand where your target stands and leave the sentence intact? If so you have written a frame, not a card. Rebuild until the target is the hinge the whole thing turns on: take it away and the scene should collapse.
    Whose situation is this, and what do they want? How does this scene illustrate the unique target meaning of the lexical item?
    What can be seen, heard, or handled here? Concrete and imageable material is recalled far better than abstract statement, and Koine is a concrete language. Even for abstract nouns, it can be beneficial to place them in a concrete and visual context.
    What is at stake, in motion, or a little unexpected? A small surprise aids recall, so long as the scene stays coherent and stays inside constraint 10.
    Would a student meeting this vocabulary/syntax/grammar item for the fortieth time find it worth reading? They will meet it that often.

    PRIORITY — this creative formulation portion will likely pull against the constraints above. Where it does, it yields to fidelity to Koine Greek Grammar, theological fidelity, etc.
    Ahead of it stand the thirteen hard constraints. No amount of vividness buys an uncovered form, an unknown word, or a second retrieval demand.
    Ahead of everything stands real, accurate Koine. Reaching for an imaginative scene that is grammatical on paper but alien in idiom, or straining for uniqueness to the point of unusual is equally unhelpful. The student must be able to meet this construction in the corpus' own methodology of unique and creative crafting, despite the sentence not actually being derived from the corpus.
    A flat sentence in real Koine is a poor card. A vivid sentence in Greek that does not cover the lexeme properly, or one that utilizes grammar foreign to Koine, is a poor card. Moreover it teaches the student something false.
    Correct Koine first, then the constraints, then make it worth reading.

  OUTPUT FORMAT — return ONLY a JSON object wrapped in triple backticks, with nothing before or after it:

  ```json
  { ... }
  ```

  Every card includes these six keys:
    "reasoning"    — the editorial note on this card per constraint 8; audit only, never shown to the student
    "sentence"     — the Koine Greek sentence
    "translation"  — English translation of the full sentence
    "target_form"  — the exact inflected form of the target as it appears in "sentence", copied verbatim
    "lemmas"       — every word of "sentence" in its lexical form, the target included, each once; this is what constraint 3 and the echo check are run against, so leave none out
    "setting"      — the id of the setting you built the scene in, from "setting_options", or "adapted:<id>" if you had to adapt it

  The per-card instructions below may name further keys or have further clarifications and instructions. Those go in the SAME JSON object, alongside the six above — not nested, not in a second object. Include every key named for that card type and no others. The examples in the card instructions show only the first four keys; include "lemmas" and "setting" all the same.

  As for specific card generation instructions, here are the parameters to follow:
CARD TYPE: Text Recall, Vocabulary, Greek-to-English.
You must create a phrase/short sentence for the student. The student will eventually read the sentence and recalls what the target word means. The sentence is the only cue, so the surrounding context you create must make the target's sense recoverable without giving it away outright. Your sentence does not necessarily have to use the item in lexical form; it can vary according to best usage contextually as long as the form is reasonably recognizable since the student has access to the lexical form.

EXAMPLES — one card of this type at each level, all for an unrelated card item, each delevoped independently for ἄρτος. You write ONE card; the three stand here only to show what changes with level and what does not.
beginner:
```json
{
  "reasoning": "The main ln entry specifies that ἄρτος is a small loaf of bread. Contextually it sits in the domain of food and condiments, specifically food. 5.6 and 5.7 signify satisfying drinks and solid food or meat. 5.9 and 5.10 signify two forms of wheat flour. ἄρτος seems to be in-between satisfying and filling food and unprepared culinary materials, sigifying it is a basic and cheap staple. A helpful and creative context for this could be a beggar with bread. This fulfills the condition of the swap test as opposed to some other substantial food item or satisfying drink. The information provided specifies the student is at a beginner level, so a simple sentence with reasonable vocabulary and morphologically expected tense forms must be preserved.",
  "sentence": "ὁ πτωχὸς αἰτεῖ ἄρτον.",
  "translation": "The beggar asks for bread.",
  "target_form": "ἄρτον"
}
```
beyond_beginner:
```json
{
  "reasoning": "The main ln entry specifies that ἄρτος is a small loaf of bread. Contextually it sits in the domain of food and condiments, specifically food. 5.6 and 5.7 signify satisfying drinks and solid food or meat, while 5.9 and 5.10 signify two forms of wheat flour. Sitting between what satisfies hunger and what is merely raw material, ἄρτος is the ordinary staple one expects to have on hand, which means its absence is felt as plain hunger rather than as the loss of a luxury. A helpful and creative context for this could be travellers running short of it on a journey, with hungry children making the lack concrete rather than abstract. This fulfills the condition of the swap test, since a drink or a measure of flour would not produce hunger in the same immediate way. The information provided specifies the student is beyond beginner, so the scene can be carried across two coordinated clauses with a prepositional phrase, and the imperfects are morphological forms within this student's reach.",
  "sentence": "οὐκ εἴχομεν ἄρτον ἐν τῇ ὁδῷ, καὶ ἐπείνων οἱ παῖδες.",
  "translation": "We had no bread on the road, and the children were hungry.",
  "target_form": "ἄρτον"
}
```
advanced:
```json
{
  "reasoning": "The main ln entry specifies that ἄρτος is a small loaf of bread, and notes it is considerably smaller than a present-day loaf. Contextually it sits in the domain of food and condiments, specifically food. 5.6 and 5.7 signify satisfying drinks and solid food or meat, while 5.9 and 5.10 signify two forms of wheat flour. A staple that is already portioned and small enough to carry is something a person can hold, move, and keep from someone else, which raw flour and a drink are not. A helpful and creative context for this could be a woman hiding one under her cloak as soldiers approach, where the concealment itself argues for something both worth taking and small enough to conceal. This fulfills the condition of the swap test, since flour could not be hidden in a garment and a drink would not survive the gesture. The information provided specifies the student is advanced, so the scene is built as running prose with a genitive absolute setting the hour and a purpose clause supplying the motive, both forms this student reads in the corpus.",
  "sentence": "τοῦ ἡλίου δύνοντος, ἡ γυνὴ ἔκρυψεν τὸν ἄρτον ὑπὸ τὸ ἱμάτιον, ἵνα μὴ ἴδωσιν οἱ στρατιῶται.",
  "translation": "As the sun was setting, the woman hid the bread under her cloak, so that the soldiers would not see it.",
  "target_form": "ἄρτον"
}
```
What holds across all three: the target is the hinge, and removing it collapses the scene. What changes is only the surrounding texture. Do not carry these scenes, their vocabulary, or their shapes into your own card — your item, its supplied data, and the student block decide what you write.
The following single item up for review from the previous card instructions is in an JSON object carrying:
  "item"                — the item under review and everything known about it, including its hand-vetted reference card. Extra information included is to benefit to creation of the individual task item, not for creating cards for every piece fed in.
  "recent_generations"  — cards already produced for this item; constraint 11 forbids repeating or paraphrasing them (in the case there is no history of review this will be empty)
  "student"             — where this student currently stands:
      "level"              — "beginner", "beyond_beginner", or "advanced"; this is the level constraint 7 refers to
      "concepts_learned"   — what has been covered: "grammar" names the morphology the student can form, by paradigm (e.g. "First Aorist Passive Indicative", "Relative Pronoun"), and "syntax" the syntactic categories met; constraint 4 binds you to these and to nothing outside them
      "vocabulary_learned" — the words available to you, or "Not Applicable"
  "sentence_plan"       — the shape the sentence takes, what else it carries, and where it takes place; see SENTENCE PLAN below

BEGINNER — one short main clause. For reference, not as a hard constraint, it could utilize present or imperfect indicative, explicit subject where it helps, no participles, no subordination. Nothing in the clause should need decoding except the target.
BEYOND_BEGINNER — the full range permitted by "concepts_learned": vary case, tense, mood and word order, and use prepositional phrases and subordinate clauses. Reach for this range rather than staying safe; a card built from bare elementary vocabulary at this level teaches less than it could.
ADVANCED — write Koine as the corpus actually runs. Participial chains, genitive absolutes, indirect discourse, correlative and relative structures, marked word order — whatever "concepts_learned" permits. The sentence should read as prose a student will actually meet, not as a drill.

Whatever the level, the target itself stays unambiguous. Raising the level raises the surrounding texture, never the difficulty of identifying what is being asked.

When "vocabulary_learned" is "Not Applicable" no explicit word list is available. Judge what the student can read from "level" and "concepts_learned", and stay well inside it rather than at its edge.

SENTENCE PLAN — "sentence_plan" was drawn before you were called, from what this student has learned. Follow it. Where it and the level guidance above differ, the plan wins.
  "sentence_shape"  — the structure of the sentence: a single main clause, a main clause with the dependent or relative clause it names, or two coordinated clauses. "formation" and "function" say how the construction is built and what it does, "syntactic_category" names the usage and gives the grammars' syntactic explanation of it, and "position" says where it normally stands. Where a "paradigm" is given, form the construction from that chart: it holds the forms this student has learned, on the paradigm verb and on the contract, liquid and athematic verbs the grammars print beside it, and constraint 12 makes it authoritative. The shape carries the sentence; the target sits in whichever clause suits it and stays the one thing the card asks about.
  "also_include"    — further syntactic usages this student has learned, each named with its place in the grammars' taxonomy and its syntactic explanation. Work each in once and naturally. They are texture, never a second retrieval demand: the card does not ask about them, and none may compete with the target for the student's attention.
  "setting_options" — two everyday situations. Choose the one the item lives in most naturally and write the scene inside it. If neither can hold the item without strain, adapt the closer one: keep its kind of people and place, change what happens. Report which in "setting".
Everything the plan leaves open is yours: the verb, its subject and object, every other word. Choose them because they belong together in the setting and the student can read them — not because a verse puts them together.

Here is the relevant item to form the card for:
```

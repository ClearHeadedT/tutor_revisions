

SENTENCE_TYPE_WEIGHTS = {
    "simple_beginner_sentence": 0.2,
    "main_and_dependent_sentence": 0.6,
    "main_and_relative_sentence": 0.4,
    "two_complete_coordinating_sentence": 0.2
}

TIER_WEIGHTS = {"regular": 1.0, "occasional": 0.2, "rare": 0.04}

# From counts of each construction in N1904; adverbial participles and result ἵνα, which a form
# cannot sort by meaning, from the grammars. Anything unlisted is regular.
USAGE_TIERS = {
    "main_and_dependent_sentence.adverbial.causal.infinitive": "occasional",
    "main_and_dependent_sentence.adverbial.concessive.adverbial_participle": "occasional",
    "main_and_dependent_sentence.adverbial.concessive.ei_kai_indicative": "occasional",
    "main_and_dependent_sentence.adverbial.conditional.second_class": "occasional",
    "main_and_dependent_sentence.adverbial.manner_means.articular_infinitive": "rare",
    "main_and_dependent_sentence.adverbial.manner_means.relative_pn_hon": "rare",
    "main_and_dependent_sentence.adverbial.purpose.adverbial_participle": "occasional",
    "main_and_dependent_sentence.adverbial.purpose.relative_pn_hoitines": "rare",
    "main_and_dependent_sentence.adverbial.resultative.infinitive": "occasional",
    "main_and_dependent_sentence.adverbial.resultative.adverbial_participle": "occasional",
    "main_and_dependent_sentence.adverbial.resultative.hina_subjunctive": "rare",
    "main_and_dependent_sentence.adverbial.resultative.relative_adverb_hothen": "rare",
    "main_and_dependent_sentence.adverbial.time.articular_infinitive": "occasional",
    "main_and_dependent_sentence.adverbial.time.relative_pn": "occasional",
    "main_and_dependent_sentence.adverbial.local.hopou_indicative": "occasional",
    "main_and_dependent_sentence.adverbial.local.relative_adverb_hou": "occasional",
    "main_and_relative_sentence.substantival.subjunctive": "occasional",
}

FREQUENCY_NOTES = {
    "occasional": "Not frequent in the New Testament. Be aware of that: stay true to its form while "
                  "keeping the sentence reasonable.",
    "rare": "Rare in the New Testament. Build it exactly to its formation and keep the rest of the "
            "sentence plain.",
}

GRAMMAR_EXAMPLES = 3

LEVEL_PLANS = {
    "beginner": {"shape": False, "extra": False},
    "beyond_beginner": {"shape": True, "extra": True},
    "advanced": {"shape": True, "extra": True},
}
EXTRA_CHANCE = 0.75
EXTRA_OPTIONS = 3

# Grammar groups a main clause cannot carry by itself, by the end of the group key. A card on one is
# built on a construction that takes it; a participle or infinitive may instead stand in a single
# main clause, attributively, substantivally or as a complement.
HOSTED_GROUPS = ("-subj", "-ptc", "-inf", "pronoun-relative")
MAIN_CLAUSE_GROUPS = ("-ptc", "-inf")

# Card types whose sentence is the whole exercise: the student writes it, or judges it. These get
# a single main clause and nothing extra.
PLAIN_CARD_TYPES = {"self_formulation_syntax_e2g", "validity_judgment_syntax_g2e"}

SETTING_OPTIONS = 2

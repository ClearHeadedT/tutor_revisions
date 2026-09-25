

SENTENCE_TYPE_WEIGHTS = {
    "simple_beginner_sentence": 0.2,
    "main_and_dependent_sentence": 0.6,
    "main_and_relative_sentence": 0.4,
    "two_complete_coordinating_sentence": 0.2
}

# Weights for the categories below a sentence type. A name missing here is drawn at 0.1.
CATEGORY_WEIGHTS = {
    # adverbial dependent clauses
    "causal": 0.4,
    "concessive": 0.3,
    "conditional": 0.2,
    "manner_means": 0.4,
    "purpose": 0.4,
    "resultative": 0.4,
    "time": 0.2,
    "comparative": 0.15,
    "local": 0.15,
    # relative clauses
    "adjectival": 0.6,
    "substantival": 0.4,
    "indicative": 0.6,
    "subjunctive": 0.4,
    # single-child nodes
    "adverbial": 1.0,
    "connector_piece": 1.0,
}

# What a plan may carry at each level: whether the sentence shape is drawn at all, and how many
# extra constructions it may ask for. Each extra is included with EXTRA_CHANCE, so a
# beyond_beginner plan carries none about half the time.
LEVEL_PLANS = {
    "beginner": {"shape": False, "extras": 0},
    "beyond_beginner": {"shape": True, "extras": 1},
    "advanced": {"shape": True, "extras": 2},
}
EXTRA_CHANCE = 0.5

# Card types whose sentence is the whole exercise: the student writes it, or judges it. These get
# a single main clause and nothing extra.
PLAIN_CARD_TYPES = {"self_formulation_syntax_e2g", "validity_judgment_syntax_g2e"}

# How many settings a plan offers the model to choose between.
SETTING_OPTIONS = 2

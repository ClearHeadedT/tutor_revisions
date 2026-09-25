"""The fixed sample the harness generates cards for.

Ten of each category, chosen to be as unlike each other as the data allows, so that a
weakness in the instructions shows up somewhere in the run rather than hiding behind a
set of near-identical items.
"""

# All three rules, all four cases, all three genders, singular and plural, and all
# three persons -- the widest spread the 38 available slots permit.
GRAMMAR_ITEMS = [
    "article::ὁ::nominative.masculine.singular",
    "article::ἡ::genitive.feminine.singular",
    "article::τό::dative.neuter.plural",
    "article::ἡ::accusative.feminine.plural",
    "decl2::λόγος::nominative.singular",
    "decl2::λόγος::dative.singular",
    "decl2::λόγος::accusative.plural",
    "pres-act-ind::λύω::first_person.singular",
    "pres-act-ind::λύω::second_person.plural",
    "pres-act-ind::λύω::third_person.plural",
]

# One core usage from each of ten different categories, so no two share a parent and
# the sibling material differs completely between them.
SYNTAX_ITEMS = [
    "genitive/adjectival/descriptive-genitive",
    "dative/pure-dative-uses/dative-indirect-object",
    "accusative/substantival-uses-accusative/accusative-direct-object",
    "article/regular-uses-article/as-pronoun-partially-independent-use/personal-pronoun",
    "voice/active/simple-active",
    "moods/indicative/declarative-indicative",
    "tense/present/instantaneous-present-k-aoristic-punctiliar-present",
    "participle/substantival-independent",
    "conjunctions/ascensive",
    "conditional-sentences/ii-conditional-sentences-greek-especially-nt/first-class-condition",
]

# (form Text-Fabric indexes, conventional lexicon entry).
# Four verbs, four substantives, two others, all of them ordinary GNT vocabulary.
VOCABULARY_ITEMS = [
    ("βαπτίζω", "βαπτίζω"),
    ("κράζω", "κράζω"),
    ("διώκω", "διώκω"),
    ("θεραπεύω", "θεραπεύω"),
    ("θύρα", "ἡ θύρα"),
    ("ποιμήν", "ὁ ποιμήν"),
    ("σκότος", "τὸ σκότος"),
    ("μάχαιρα", "ἡ μάχαιρα"),
    ("πιστός", "πιστός, -ή, -όν"),
    ("εὐθέως", "εὐθέως"),
]

# A syntactic category on its own does not tell the model what to build the clause out
# of, and the corpus supplies no example vocabulary, so each item carries a few lemmas
# that suit it. Ordinary words, deliberately not the ones scripture has welded to the
# construction.
SYNTAX_LEXEMES = {
    "genitive/adjectival/descriptive-genitive": ["λίθος", "ὕδωρ", "οἰκία"],
    "dative/pure-dative-uses/dative-indirect-object": ["παιδίον", "δοῦλος", "γυνή"],
    "accusative/substantival-uses-accusative/accusative-direct-object": ["ἄρτος", "θύρα", "ἐπιστολή"],
    "article/regular-uses-article/as-pronoun-partially-independent-use/personal-pronoun": ["μαθητής", "ὄχλος", "στρατιώτης"],
    "voice/active/simple-active": ["γράφω", "διώκω", "θεραπεύω"],
    "moods/indicative/declarative-indicative": ["βλέπω", "ἀκούω", "μένω"],
    "tense/present/instantaneous-present-k-aoristic-punctiliar-present": ["λέγω", "παρακαλέω", "ἀσπάζομαι"],
    "participle/substantival-independent": ["πιστεύω", "ἀκολουθέω", "ἐργάζομαι"],
    "conjunctions/ascensive": ["τελώνης", "παιδίον", "πτωχός"],
    "conditional-sentences/ii-conditional-sentences-greek-especially-nt/first-class-condition": ["υἱός", "ἔργον", "ἀληθής"],
}

# The sample is run against a hypothetical student described by level alone. A literal
# list of the five words austin has actually met reads to the model as the whole of the
# language available to it, which is worse than giving no list at all -- constraint 3
# and instructions_cap both provide for judging by level instead.
TEST_STUDENT = {
    "level": "beyond_beginner",
    "concepts_learned": "Not Applicable",
    "vocabulary_learned": "Not Applicable",
}

CARD_TYPES = {
    "grammar": "text_recall_grammar_g2e",
    "vocabulary": "text_recall_vocabulary_g2e",
    "syntax": "function_recall_syntax_g2e",
}

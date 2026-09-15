from text_fabric.fabric_utils import load_n1904, find_ln_entry
from greek_text import normalize_greek




def word_search(words):
    """Returns the relevant nodes of a particular word in the corpus"""
    A = load_n1904()
    results = {}
    for word in words:
        word = normalize_greek(word)
        hits = [n for n in A.api.F.otype.s('word') if normalize_greek(A.api.F.lemma.v(n) or "") == word]
        results[word] = hits
    return results


def word_internals_breakdown(nodes):
    """Parses out the internal word information from their nodes"""
    A = load_n1904()
    
    


def word_enrichment(word):
    """Parses out the internal word information from both TF and Louw-Nida functionality"""
    A = load_n1904()
    word_nodes = [n for n in A.api.F.otype.s('word') if normalize_greek(A.api.F.lemma.v(n) or "") == word]
    sense_usages = {}
    for node in word_nodes:
        sense = A.api.F.ln.v(node)
        for ln in sense.split():
            if ln in sense_usages:
                sense_usages[ln] += 1
            else:
                sense_usages[ln] = 1
    if not sense_usages:
        return None
    enriched_word = {}
    highest_sense = max(sense_usages, key=sense_usages.get)
    for sense in sense_usages.items():
        ln_entry = find_ln_entry(sense)
        
    print("\n\n")
    print(highest_sense)







# ======== FIRST - BUILDING THE WORD'S INTERNALS WITH TF BITS AND SENSE CONTEXT/SYNONYMS ========

# Word search return functionality definition-builder:
    # Need to begin with volume 2 Greek all senses 
        # Decide the primary sense domain
            # Find the most relevant of them??
            # Probably do an internal search utilizing TF to find how many occurrences there are per sense usage
            # Highest sense occurrence will be the primary sense learned on initial card 
        # Search functionality to grab the sense definitions from each of these sense entries in volume 1 
            # Traversing volume 1 through recursion to grab contextual information markers and the definition itself 
            # Once id found, grabbing the id of the previous 3 and next 3 for comparison analysis
                # Get definitions, id, w/e else
                # Some potential problem resolutions:
                    # Not searching by ID since it could be the first entry
                    # Have to traverse by dict entry somehow not exactly sure yet
            # For secondary sense usages:
                # Put all this information in a nice formatted str and pass it back as "secondary"
                    # Figure out if all pieces are necessary or if it can be reduced - maybe contingent on how many extra sense entries 
            # For primary:
                # Put it all there 
    # For primary sense domain/word 
        # Resolve the word fully with other internal bits/information
        # Format its baseline information nicely
        # Separate into two sections the internals of the word and the Nida sense information
    # Pin the secondary senses on the end and their relevant internals 

    # Return this - not ALL of this information will go in the JSON for vocabulary_scaffolding, but all of this is the information that will be passed to LLM for card creation
        # first part with tf bits can be accessed individually for the scaffolding 


# ======== SECOND - SAVING TO SCAFFOLDING JSON AND LLM CALL ========

    # variable initialization empty dict which will be put into JSON eventually 
    # For each lexeme 
        # feed lexeme into sense/bits function
        # make entry in dict for it with empty 'reference_sentence' card
            # use only the first portion of the returned value from function which contains the bits info 
        # do llm call for initial card formation - simple first card type. Feeding in BOTH parts of the prior function 
        # Add that LLM result to the reference_sentence portion in the dict 
    # Make the dict into JSON format
    # Save/write the information into the scaffolding file





# important stuff from nida 
    # two volumes:
        # First volume by sense domain with individual words in their domains (in multiple places if applicable)
        # Second volume two parts:
            # Greek-English Index - 
                # basic gloss
                # List of all sense possibilities if more than the one exist 
                # link to volume 1 entry for each of those sense possibilites
            # English-Greek Index - 
                # English word 
                # simple number entry for the senses in volume 1 that contain this English word sense idea 




    # Analyzes ln: 
        # particular domain
        # most common usage/definition
        # other adjascent common sense usages for same word 
        # Near synonyms 
            # Linguistic theory - contrast with these. Different for a reason, could have used X instead of Y
    # "resolves" a word fully as seen below
        # ALL bits of internal information








"""Reference for the CenterBLC/N1904 Text-Fabric dataset.

Everything below was measured from the dataset itself, not taken from documentation.
Load it with load_n1904() in load_client.py -- roughly 9 seconds per process, so load
once and pass the app around rather than calling it inside a helper.

ACCESS API
    A = load_n1904()
    F, L, T, S, E = A.api.F, A.api.L, A.api.T, A.api.S, A.api.E

    F.lemma.v(node)             one feature on one node
    Fs("lemma").v(node)         same, when the feature name is in a variable
    F.otype.s("word")           every node of a type
    F.case.freqList()           value -> count, sorted descending
    L.u(word, otype="clause")   walk UP the tree from a node
    L.d(verse, otype="word")    walk DOWN
    E.parent.f(node)            edges: parent, sibling, frame, subjref, oslots
    T.text(node)                surface text of any node
    T.nodeFromSection(("John", 1, 1))
    S.search(template)          TF search

TWO GOTCHAS
    F.lemma.v() is 87% non-NFC -- 4,681 of 5,396 distinct lemmas. Run every lemma
    through greek_text.normalize_greek() before comparing or joining against our
    scaffolding keys. Normalizing produces no collisions (5,396 distinct either way).

    F.strong.v() returns an int, not a string.

NODE TYPES, largest to smallest span
    book 27 | chapter 260 | verse 7,944 | sentence 8,011 | group 8,945
    clause 42,506 | wg 106,868 | phrase 69,007 | subphrase 116,178 | word 137,779

    "wg" is wordgroup. The Macula syntax tree is genuinely native here, not a
    side-load: sentence -> group -> clause -> wg -> phrase -> subphrase -> word.

WORD FEATURES -- 44 of the dataset's 56 features carry values on word nodes.
Coverage is the percentage of words carrying a value.

    surface       text (with trailing space), unicode (incl. following material),
                  unaccent, translit, normalized, after, trailer, punctuation,
                  criticalsign
    lexical       lemma, lemmatranslit, strong, gloss (BGVB), trans (Berean
                  interlinear rendering of this token, not the lexical gloss)
    morphology    morph (packed code, e.g. N-NSM) plus the unpacked features below
    semantics     ln (Louw-Nida, 97.5%, e.g. "33.100"), domain (zero-padded, "033006")
    syntax        role 36%, function 36%, rela, framespec, referent, subjrefspec,
                  discontinuous
    location      book, bookshort, chapter, verse, ref ("JHN 1:1!5"),
                  id ("n43001001005"), num

    Note that mood carries infinitive and participle, so neither is a separate
    part of speech in sp/cls.

SYNTAX ABOVE THE WORD
    role and function are sparse on words because they mostly sit on the enclosing
    nodes. Walk up with L.u() and read: role, rule, crule, cltype, clausetype,
    junction, typ, articular.

ONE WORD, FULLY RESOLVED (John 1:1, Λόγος)
    lemma=λόγος  strong=3056  morph=N-NSM
    sp=subs  cls=noun  case=nominative  gender=masculine  number=singular
    typems=common  gloss='word, speech'  trans='Word'
    ln=33.100  domain=033006  ref='JHN 1:1!5'  id='n43001001005'
"""

NODE_TYPES = (
    "book", "chapter", "verse", "sentence", "group",
    "clause", "wg", "phrase", "subphrase", "word",
)

# Complete value sets, measured across all 137,779 word nodes.
# Percentage is coverage: how many words carry the feature at all.
SP = ("adjv", "advb", "art", "conj", "intj", "num", "prep", "pron", "subs", "verb")   # 100%
CLS = ("adj", "adv", "conj", "det", "intj", "noun", "num", "prep", "pron", "ptcl", "verb")  # 100%
CASE = ("nominative", "genitive", "dative", "accusative", "vocative")                 # 57%
GENDER = ("masculine", "feminine", "neuter")                                          # 53%
NUMBER = ("singular", "plural")                                                       # 73%
PERSON = ("p1", "p2", "p3")                                                           # 16%
TENSE = ("present", "imperfect", "future", "aorist", "perfect", "pluperfect")          # 22%
VOICE = ("active", "middle", "passive", "middlepassive")                              # 22%
MOOD = ("indicative", "subjunctive", "optative", "imperative", "infinitive", "participle")  # 22%
DEGREE = ("comparative", "superlative")                                               # 0.4%
TYPEMS = ("common", "proper", "personal", "possessive", "demonstrative",
          "relative", "interrogative", "indefinite", "adverbial")                     # 31%

# Syntactic role and function, as they appear on words and on enclosing nodes.
ROLE = ("v", "vc", "s", "o", "o2", "io", "p", "adv", "aux", "apposition")             # 36%
FUNCTION = ("Subj", "Pred", "Objc", "Cmpl", "Adv", "PreC")                            # 36%

EDGE_FEATURES = ("parent", "sibling", "frame", "subjref", "oslots")

# Distinct-value counts worth knowing before writing a query.
DISTINCT = {
    "lemma": 5396,
    "strong": 5339,
    "gloss": 5202,
    "morph": 1055,
    "text": 19446,
    "unaccent": 18148,
    "ln": 7816,
    "domain": 1648,
}

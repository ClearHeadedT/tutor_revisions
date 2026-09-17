from functools import cache

from text_fabric.fabric_utils import load_n1904, find_ln_entry, find_ln_surrounding_context, ln_definition
from greek_text import normalize_greek


@cache
def lemma_index():
    """Every word node in the corpus grouped by normalized lemma. Built in one pass
    and held, so enriching a hundred words costs the same scan as enriching one."""
    A = load_n1904()
    F = A.api.F
    index = {}
    for node in F.otype.s('word'):
        index.setdefault(normalize_greek(F.lemma.v(node) or ""), []).append(node)
    return index


def word_enrichment(word):
    """Parses out the internal word information from both TF and Louw-Nida functionality"""
    word = normalize_greek(word)
    return enrichment_from_nodes(word, lemma_index().get(word, []))


def word_enrichment_batch(words):
    """Enriches a list of words against a single corpus scan. This is what the
    senses cache is built from -- reaching for Text-Fabric is the expensive part,
    so a run pays for it once and enriches everything it needs."""
    return {normalize_greek(word): word_enrichment(word) for word in words}


def enrichment_from_nodes(word, word_nodes):
    """The enrichment itself, once the word's occurrence nodes are in hand."""
    A = load_n1904()
    sense_usages = {}
    for node in word_nodes:
        sense = A.api.F.ln.v(node)
        if not sense:
            continue
        for ln in sense.split():
            if ln in sense_usages:
                sense_usages[ln] += 1
            else:
                sense_usages[ln] = 1
    if not word_nodes:
        return None
    if not sense_usages:
        return {"tf_lexical_info": word_internals_breakdown(word_nodes), "ln_sense_info": None}
    highest_sense = max(sense_usages, key=sense_usages.get)
    total = sum(sense_usages.values())
    # the primary sense keeps its whole entry; the rest are trimmed to their definitions
    primary_entry = find_ln_entry(ln_num=highest_sense)
    primary = {
        "ln": highest_sense,
        "occurrences": sense_usages[highest_sense],
        "share": round(sense_usages[highest_sense] / total, 2),
        "full_entry": primary_entry["text"],
        "surrounding_context": find_ln_surrounding_context(highest_sense),
    }
    secondary = []
    for sense in sorted(sense_usages, key=sense_usages.get, reverse=True):
        if sense == highest_sense:
            continue
        entry = find_ln_entry(ln_num=sense)
        secondary.append({
            "ln": sense,
            "occurrences": sense_usages[sense],
            "share": round(sense_usages[sense] / total, 2),
            "definition": ln_definition(entry) if entry else None,
            "subdomain": (find_ln_surrounding_context(sense) or {}).get("subdomain"),
        })
    summary = (
        f"{word}: primary sense {highest_sense} "
        f"({primary['occurrences']} of {total} tagged occurrences, "
        f"{primary['surrounding_context']['domain']} / {primary['surrounding_context']['subdomain']}). "
        + (f"Secondary senses: {', '.join(s['ln'] + ' (' + str(s['occurrences']) + 'x)' for s in secondary)}."
           if secondary else "No secondary senses attested.")
    )
    enriched_word = {
        "tf_lexical_info": word_internals_breakdown(word_nodes),
        "ln_sense_info": {
            "summary": summary,
            "primary_sense": primary,
            "secondary_senses": secondary,
        },
    }
    return enriched_word


def word_search(words):
    """Returns the relevant nodes for a group of words from the corpus"""
    A = load_n1904()
    results = {}
    for word in words:
        word = normalize_greek(word)
        hits = [n for n in A.api.F.otype.s('word') if normalize_greek(A.api.F.lemma.v(n) or "") == word]
        results[word] = hits
    return results


def word_internals_breakdown(nodes):
    """Returns the lexical facts for a lemma from its occurrence nodes:
    lemma, part of speech, longest attested gloss, and GNT frequency."""
    A = load_n1904()
    F = A.api.F
    return {
        "lemma": normalize_greek(F.lemma.v(nodes[0])),
        "part_of_speech": F.cls.v(nodes[0]),
        "gloss": max((F.gloss.v(node) for node in nodes), key=len),
        "frequency": len(nodes),
    }




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

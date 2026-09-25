"""Where the pieces of a Greek sentence go.

`WORD_ORDER_INSTRUCTIONS` is the operational version - what gets handed to an LLM building a
sentence, as part of GENERAL_CARD_INSTRUCTIONS. `PORTER_SOURCE` below it is the verbatim material
it was condensed from, kept because it is the citable source. The operational version's examples
are fresh phrases rather than verses, since the card model is told not to reproduce the New
Testament and a verse in its own instructions would pull the other way; every form in them is
attested in N1904.

Two decisions are baked into the condensed version and should be known before editing it:

1. **Porter is the unmarked baseline, not Young/BDF.** They flatly disagree. Young (INTG 215),
   following BDF, gives the basic order as verb-subject-object. Porter (IDIOMS 293-97) calls that
   "probably inaccurate", arguing it is an artifact of counting only the clauses where all three
   elements happen to be expressed, and finds instead that the predicate is the minimal unit and
   that an expressed subject usually comes first. Since this generator always expresses subject,
   verb and object, Porter's finding applies directly and yields S-V-O.

2. **A dependent clause's position follows its meaning, not its form.** INTG 216: "it does not
   make any difference whether the clause is formed with a finite verb ... or with a non-finite
   verb (participle or infinitive)." A conditional participle precedes and a result participle
   follows, exactly as the matching conjunction would. This is why JSON_skeleton.py hangs
   `default_position` on the semantic type (causal, purpose) rather than on the realization
   (infinitive, adverbial_participle, oti_indicative).

The before/after table in section 3 is corroborated by two independent grammars: INTG 216 prints
it as a chart of normal positions, and DEEPER 456 prints the same split from the opposite
direction, as a table of orders that are *possibly emphatic*. They agree on every entry.
"""


WORD_ORDER_INSTRUCTIONS = """\
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
The one exception is the causal participle, which usually precedes its verb; causal clauses with
a conjunction still follow.

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
"""


# Sources the above was condensed from. Section 1-2 and section 5's statistics are Porter,
# Idioms of the Greek New Testament, 288-297, reproduced verbatim below. Section 3's table and
# section 4's fronting triggers are Young, Intermediate New Testament Greek, 215-218; the
# emphatic-order list closing section 4 is Kostenberger et al., Going Deeper with NT Greek, 456.
PORTER_SOURCE = """
In Greek, certain words or kinds of words normally appear in established places (or slots) in the Greek clause. For example, certain words in Greek cannot (or only exceptionally) occur at the beginning of a clause. Other words in Greek normally do not end a clause. Still other words do tend to occur at the beginning of a clause.

1.3.1. The Greek article. In Greek if a substantive appears with its article, the article is placed before the substantive: e.g. ὁ θεός, not θεὸς ὁ.

1.3.2. Postpositive words. The following words tend not to begin a clause (or phrase) in NT Greek, but usually appear in the second structural position: ἄν, γάρ, δέ, γέ, μέν, οὖν, and enclitics such as ποτέ, πώς, τέ, as well as a number of pronouns (με, μου, μοι). These are often called postpositive words. Postpositive means that the word occurs anywhere from right after the first word in a syntactical unit (Mk 15.6: κατὰ δὲ ἑορτήν [and at the feast]) to after the first entire element (such as a phrase; e.g. 1 Cor. 1.18: ὁ λόγος γὰρ ὁ τοῦ σταυροῦ [for the word of the cross]), or beyond (Rom. 9.19: ἐρεῖς μοι οὖν [therefore, you will say to me]), and anywhere in between (2 Cor. 1.19: ὁ τοῦ θεοῦ γὰρ υἱός [for the son of God]). To use the language of slot and filler, the slot for a postpositive word is a large one, extending from right after the first word to and including the next place after the first entire phrase, and all points in between (and sometimes even beyond).

a. In NT Greek, some words which in classical Greek are postpositive occur first in clauses.
Lk. 11.28: μενοῦν μακάριοι οἱ ἀκούοντες τὸν λόγον (therefore, blessed are those who hear the word), where μενοῦν appears at the beginning of the clause.
1 Thess. 4.8: τοιγαροῦν ὁ ἀθετῶν οὐκ ἄνθρωπον ἀθετεῖ (therefore, the one who rejects does not reject a human being), where the connective consists of three words which are usually postpositive; Heb. 12.1: τοιγαροῦν καὶ ἡμεῖς τοσοῦτον ἔχοντες … (therefore, we indeed having such …).

  p 289  b. In NT Greek, some words which in classical Greek are not postpositive are occasionally used as if they were.
2 Cor. 2.4: τὴν ἀγάπην ἵνα γνῶτε (so that you might know the love); cf. Gal. 2.10; Col. 4.16; Acts 19.4.
Rom. 11.2: ἐν Ἠλίᾳ τί λέγει ἡ γραφή; (in [the case of] Elijah, what does the Scripture say?), where the interrogative pronoun normally occurs first.

1.3.3. Non-final words. A number of words are not normally used to end a clause in NT Greek: e.g. ἀλλά, ἤ, καί, οὐδέ/μηδέ, οὔτε/μήτε, εἴτε, μή (lest), relative pronouns, a number of indeclinable words (εἰ, ἐπεί, ἵνα, ὁ [the]), and most prepositions.

1.3.4. Fronted elements. A number of words tend to be placed near the beginning of a clause in NT Greek: interrogatives, clause negatives, words of succession (πρῶτον, ἔπειτα, εἶτα), most pronouns including demonstratives in the nominative case, νῦν, τότε, αὐτός (self), ἄλλος and ἕτερος, ἀμφότεροι, πολύς, πολλάκις, εἷς.
Rom. 1.8: πρῶτον μὲν εὐχαρτιστῶ τῷ θεῷ μου (first, I give thanks to my God).
Lk. 16.7: ἔπειτα ἑτέρῳ εἶπεν (then he said to someone else).
Rom. 1.13: ὅτι πολλάκις προεθέμην (that many times I planned).
Rom. 4.1: τί οὖν ἐροῦμεν; (what therefore shall we say?).
Rom. 4.13: οὐ γὰρ διὰ νόμου ἡ ἐπαγγελία (for the promise was not through the law); Rom. 6.12: μὴ οὖν βασιλευέτω ἡ ἁμαρτία (therefore, sin is not to rule).


2. Patterns in NT Greek Word Order and Clause Structure

The flexibility of Greek syntax because of its inflected endings and its various ways of forming clauses does not mean that the order of various elements makes no difference. This can be seen from the use of postpositives and other words and elements discussed above (section 1.3). Greek has several well-established structural patterns. There are two problems with arriving at a formulation of these, however. The first is that grammarians are not agreed on a proper method and terminology to determine and discuss word order and clause structure, and  p 290   the second is that grammarians fail to make necessary distinctions regarding clause structure. To aid in discussion below, a differentiation will be made between word order (e.g. the relation of a noun and an adjective, and the placement of individual words within clauses), clause structure (e.g. the order of subjects, predicates and complements), and sentence structure (the relation of independent and dependent clauses). At the level of word order there is much more regularity in several NT Greek writers than many grammarians have been willing to recognize, even though individual authors may reflect differing patterns. Although these conflicting data present problems for arriving at meaningful patterns for all Greek usage (even for all of the Greek of the NT), they do set useful parameters for discussion of individual NT writers.

2.1. Word Order
Word order includes the order of individual words usually within such groupings as prepositional phrases, noun phrases, verb phrases, and even clause structure. Many of the word-order patterns noted here have been mentioned elsewhere in this book, without their significance being drawn out. The results listed here are preliminary but reflect recent thought regarding the Greek of the NT, and to a very limited extent extra-biblical writers of Greek.

2.1.1. Adjectival modifier. In the Greek of the NT, the adjectival modifier follows its noun approximately 75% of the time in Luke and Mark, whether it is in attributive or predicate structure. It precedes its noun approximately 65% of the time in Paul. Thus the normal Lukan structure occurs in Lk. 15.13: χώραν μακράν (a distant land), the normal Markan structure in Mk 4.41: φόβον μέγαν (great fear), and   p 291  the normal Pauline structure in Rom. 1.13: ἐν τοῖς λοιποῖς ἔθνεσιν (among the remaining nations).

2.1.2. Demonstrative pronoun. In the Greek of the NT, the demonstrative follows its noun (or substantive) far more frequently than it precedes it, approximately 85% in Paul and 78% in Luke. Thus the normal structure occurs in Lk. 4.2: ἐν ταῖς ἡμέραις ἐκείναις (in those days), and Rom. 12.2: τῷ αἰῶνι τούτῳ (this age), as opposed to 2 Cor. 7.1: ταύτας … ἔχοντες τὰς ἐπαγγελίας (having these promises).

2.1.3. Genitival modifier. In the Greek of the NT, the genitival modifier follows its noun in Paul in 96% and in Luke in 99% of all instances. Thus the normal structure occurs in Rom. 5.5: ἡ ἀγάπη τοῦ θεοῦ (the love of God), and Lk. 1.44: ἡ φωνὴ τοῦ ἀσπασμοῦ σου (the sound of your greeting), as opposed to Rom. 11.13: ἐθνῶν ἀπόστολος (apostle of the nations).

2.1.4. Object of preposition. In the Greek of the NT, the object of a preposition virtually always follows its preposition, except for the use of such words as χάριν, χωρίς (at Heb. 12.14), and ἕνεκα (and its   p 292  various forms). These appear rarely in the NT. (The phenomenon of the object preceding its preposition [postposition] does occur with some regularity in Hellenistic Greek poetical texts outside of the NT, such as Cleanthes' Hymn to Zeus.)

2.1.5. Sentence structure. In the Greek of the NT, the relative clause follows its referent in Paul in approximately 93% and in Luke in approximately 96% of the instances. Thus Rom. 5.2: διʼ οὗ (referring to Jesus Christ, above) … ἐν ᾗ (referring to grace, above), and Acts 20.18: ἡμέρας ἀφʼ ἧς ἐπέβην εἰς τὴν Ἀσίαν (day from which I went up into Asia) follow the pattern. The same pattern holds for other dependent clauses, in which the vast majority follow their main clause, except for conditional constructions, where the tendency is for the protasis to precede the apodosis.

On the basis of the statistics and examples cited above, it can be asserted with some plausibility that the Greek of the NT is best described as a linear language, certainly for word order, but also probably for sentence structure. This means that in any given construction the governing (head) or main term has a definite tendency to precede its modifier.

2.2. Clause Structure
When discussing the order of clausal elements (subject, predicate, complement), there is still a great deal of disagreement among grammarians. Discussion of participles in Chapter 10 shows that syntax makes a significant difference in understanding the temporal relations of verb-modifying participles to their main verbs; and discussion of substantives with infinitives in Chapter 11 shows that syntax makes a  p 293   significant difference in establishing the subject and complement of an infinitive structure. Many of the reference grammars of the Greek of the NT are convinced that standard NT Greek 'word order' is verb-subject-object. One of the major problems with such analyses is caused by the failure to recognize that the majority of Greek clauses do not express all of the elements used in the formulation. For example, there are many clauses in Greek which consist of simply a verb or a noun (or noun phrase with predicate), or of a verb and an object. Greek verbs are monolectic; that is, the one form contains information regarding the verbal action (aspect, mood, voice), as well as information about the subject (even though it does not explicitly specify or express that subject). It can only skew the results for determining clause structure if one presupposes some idea of where the non-expressed subject would fall in the clause, as some grammarians seem to do. The second major problem with most formulations of clause structure is that to base one's formulation of standard order on instances where all three elements are present misrepresents the evidence and the results. The minimal forms necessary for a Greek clause (e.g. subject or predicate, consisting of noun, adjective, verb) should also be used to formulate generalities regarding clause structure.
Although the following results are still very tentative, there is good reason to analyze clause structure in NT Greek in the following way. In independent and dependent clauses (so far the results do not warrant differentiating structural patterns of these clauses), the two most frequent patterns (in no designated order) are simply predicate and predicate-complement structures. These are followed (again in no designated order) by complement-predicate and subject-predicate structures. In other words, the most common patterns are when a verb or a verb and its object (with their accompanying modifiers) are used. Monolectic verbs in Greek make it understandable that predicate and   p 294  complement elements form the basic necessary units, since the verb cannot supply information about the object as it can about the subject. Depending upon the passages, the predicate-complement and complement-predicate structures are often quite close in ratio of usage.

2.2.1. Predicate structure.
1 Cor. 13.8: … καταργηθήσονται … παύσονται … καταργηθήσεται (… they will be eliminated … they will cease … they will be eliminated), in predicate structures; their subjects are all expressed in preceding verbless protases.
2 Cor. 11.4: καλῶς ἀνέχεσθε (you bear [it] well).
Phil. 2.17: χαίρω καὶ συγχαίρω πᾶσιν ὑμῖν (I rejoice and I rejoice with you all), two examples of predicate structure.

2.2.2. Predicate-complement structure.
Mt. 5.17: μὴ νομίσητε ὅτι … (don't think that …).
Rom. 6.13: μηδὲ παριστάνετε τὰ μέλη ὑμῶν ὅπλα ἀδικίας τῇ ἁμαρτίᾳ, ἀλλὰ παραστήσατε ἑαυτοὺς τῷ θεῷ (don't offer your members as instruments of unrighteousness to sin, but offer your-selves to God).
Phil. 2.2: πληρώσατέ μου τὴν χαράν (fulfil my joy).

2.2.3. Complement-predicate structure.
Mt. 6.11: τὸν ἄρτον ἡμῶν τὸν ἐπιούσιον δὸς ἡμῖν σήμερον (give our daily bread to us today).
1 Cor. 13.1: ἀγάπην δὲ μὴ ἔχω (but I do not have love).
Phil. 1.9: καὶ τοῦτο προσεύχομαι (I am praying this).

2.2.4. Subject-predicate structure.
1 Cor. 13.4a: ἡ ἀγάπη μακροθυμεῖ (love is patient), but cf. v. 4b with reverse order (and punctuation variants); 1 Cor. 13.8: ἡ ἁγάπη οὐδέποτε πίπτει (love never fails).
1 Tim. 2.11: γυνὴ ἐν ἡσυχίᾳ μανθανέτω ἐν πάσῃ ὑποταγῇ (let a woman learn in quietness in total obedience); 1 Tim. 2.13: Ἀδὰμ γὰρ πρῶτος ἐπλάσθη (for Adam was formed first); 1 Tim. 2.14: καὶ  p 295   Ἀδὰμ οὐκ ἠπατήθη, ἡ δὲ γυνὴ … ἐν παραβάσει γέγονεν (and Adam was not deceived, but the woman … was in sin).


2.3. Conclusions
If these are the normal patterns in NT Greek word order, clause structure and sentence structure, there are several noteworthy consequences. With regard to word order, the patterns noted above tend to occur with high frequencies. These must be considered the normal or non-descript ('unmarked') word-order patterns. In analysis of a given biblical writer, it is not incumbent upon the exegete to explain the normal patterns of usage, but to explain the instances which depart from these patterns (that is, the 'marked' instances).
With regard to clause structure, the most important observation is that Greek bases its structure upon the predicate as its minimal unit. One of the emphases of this grammar book has been to appreciate the significance of Greek verbal usage. The importance of the verb for Greek is confirmed by the central place occupied by the predicate in clause structure. The second-most-basic element of structure is the complement, which may occur either before or after the predicate in roughly equal proportions, although apparently with a slightly higher proportion of complements following rather than preceding the predicate. When the subject is expressed, the most common pattern for the Greek of the NT is for the subject to occur first, especially in subject-predicate structure but also in such structures as subject-predicate-complement and subject-complement-predicate. Thus, according to these findings, the frequent analysis of NT Greek clause structure as verb-subject-object is probably inaccurate. In dependent clauses, which tend to have a greater number of expressed subjects, the subject definitely tends to occur first because the expressed subject is often a relative pronoun.
These findings point to the expressed subject as an important element of Greek clause structure. The expressed subject is often used as a form of topic marker or shifter (in a 'topic and comment sequence'), and is appropriately placed first to signal this semantic function. What this means is that when the subject is expressed it is often used either to draw attention to the subject of discussion or to   p 296  mark a shift in the topic, perhaps signalling that a new person or event is the center of focus. Then comment is made upon this topic by means of the predicate. The subject gives new or emphatic information and the predicate elucidates it. For example, in 1 Tim. 2.13–14, Adam and Eve are both introduced as subjects of discussion. When statements are made about each, Adam is the expressed subject in v. 14a, then 'the woman' is mentioned in v. 14b. In each clause of v. 14 the subject is placed in initial position apparently to mark this emphasis or shift from the outset of the clause, minimizing any potential ambiguity. The rest of the clause (centered upon the predicate) then comments upon this marked or shifted topic. In Phil. 2.6 (part of a supposed hymn) the relative pronoun (ὅς) refers to Jesus Christ in v. 5, and this subject is maintained in all of the clauses until v. 9, where ὁ θεός is used in a subject-complement-predicate structure. As Hawthorne says of v. 9, 'there is a radical change in the hymn. Whereas the first half spoke of Christ as the acting subject of all the verbs, now in the last half "it is God who acts and Christ is the object of the divine action" (Beare).' Hawthorne's statement can be confirmed by analysis of clause structure.
When the subject is placed in the second or third position in the clause (i.e. after the predicate and/or complement), its markedness or emphasis apparently decreases. The reason for this is related to the linear structure of NT Greek, in which the first position is reserved for the most important element. Moving the subject to a subsidiary position, however, does not necessarily elevate another element in the clause to a position of prominence. Placing, for example, the predicate (the basic structural element) first or the complement first does not necessarily draw attention to either element, since the resulting pattern is very similar to the two basic clause structure patterns. This movement of clause elements does decrease the importance of the subject, however, relegating it to a secondary position as a topic marker. Further examples with the expressed subject include the following.
Phil. 4.5: τὸ ἐπιεικὲς ὑμῶν γνωσθήτω πᾶσιν ἀνθρώποις (let your patience be known to all people), with subject-predicate-complement structure, and the imperative in second position.
Phil. 1.15: τινὲς … τὸν Χριστὸν κηρύσσουσιν (some … are preaching Christ), with subject-complement-predicate structure.
  p 297  Jn 17.4: ἐγώ σε ἐδόξασα ἐπὶ τῆς γῆς (I glorify you on the earth), with subject-complement-predicate structure; cf. Jn 17.5: καὶ νῦν δόξασόν με σύ (and now, glorify me), with predicate-complementsubject structure. There is a distinct tendency in clauses with imperatives for the predicate to be fronted.
Rom. 11.17, 23: σὺ δὲ ἀγριέλαιος ὢν ἐνεκεντρίσθης … κἀκεῖνοι δέ, ἐὰν μὴ … ἐγκεντρισθήσονται (but you, being a wild olive, were grafted … but they, unless … will be grafted), subject-predicate structure, with intervening elements such as the participle structure and the conditional clause.
Mt. 3.2: ἢγγικεν … ἡ βασιλεία τῶν οὐρανῶν (the kingdom of heaven is near), with predicate-subject structure.
Mt. 10.5: τούτους τοὺς δώδεκα ἀπέστειλεν ὁ Ἰησοῦς (these twelve Jesus sent), with complement-predicate-subject structure.
"""

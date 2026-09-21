
# Formation instructions, keyed by the dotted path into JSON_skeleton.traversal.
#
#   formation    how the construction is built - the parts, their forms, and their order
#   function     what it does and how to render it
#   example_ref  a verse pointer only, never biblical text
#   note         only where something needs flagging
#
# Content is drawn from the reference grammars and restated; the technical substance is theirs,
# the wording here is not lifted from them.


formation_instructions = {

    # ---- adverbial dependent clauses -----------------------------------------------------
    # An adverbial clause modifies a verb. Four structures can carry the job: an infinitival
    # clause, an adverbial participial clause, a conjunctive clause, or a relative pronoun /
    # relative adverb clause. Not every function accepts all four.

    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.causal.infinitive": {
        "formation": "διὰ τό followed by an infinitive.",
        "function": "Gives the reason the controlling verb's action happened. Render it with "
                    "'because' plus a finite verb in English.",
        "example_ref": "Jas 4:2",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.causal.adverbial_participle": {
        "formation": "Anarthrous participle matching its subject in case, number and gender. "
                     "It usually sits ahead of the verb it modifies.",
        "function": "Supplies the ground or reason for the finite verb - it answers 'Why?'. "
                    "Render with 'because'.",
        "example_ref": "Rom 5:1",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.causal.oti_indicative": {
        "formation": "ὅτι plus a verb in the indicative. γάρ, διότι, ἐπεί, ἐπειδή, ἐπειδήπερ, "
                     "καθώς and ὡς can head the same kind of clause.",
        "function": "States the basis or ground on which the main clause rests. Render with "
                    "'because' or 'since'.",
        "example_ref": "Eph 4:25",
    },

    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.concessive.adverbial_participle": {
        "formation": "Anarthrous participle matching its subject in case, number and gender.",
        "function": "Concedes something: the main verb holds true in spite of what the "
                    "participle describes. Render with 'although'.",
        "example_ref": "Phil 2:6",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.concessive.ei_kai_indicative": {
        "formation": "εἰ καί plus a verb in the indicative. καὶ εἰ, κἄν and καίπερ work the "
                     "same way.",
        "function": "Grants a point without giving up the main clause - what follows stays true "
                    "even though the concessive clause is granted. Render with 'even if' or "
                    "'although'.",
        "example_ref": "Luke 11:8",
    },

    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.conditional.first_class": {
        "formation": "Protasis: εἰ plus the indicative, in any tense. Apodosis: any mood or "
                     "tense.",
        "function": "The speaker takes the condition as true so the argument can proceed from "
                    "it, and the apodosis then follows naturally. This is not the same as "
                    "'since', and it is not a bare logical connection - the protasis may in fact "
                    "be false and still be granted for the sake of the argument.",
        "example_ref": "Gal 5:18, 25; Luke 4:3",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.conditional.second_class": {
        "formation": "Protasis: εἰ plus a secondary tense of the indicative, normally aorist or "
                     "imperfect. Apodosis: usually ἄν with the indicative in the same secondary "
                     "tense.",
        "function": "The speaker takes the condition as untrue and then says what would have "
                    "been the case had it been true. Contrary to fact.",
        "example_ref": "John 5:46; 11:32",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.conditional.third_class": {
        "formation": "Protasis: ἐάν plus the subjunctive. Apodosis: any mood or tense.",
        "function": "Covers a wide band, from a purely hypothetical case to a probable one, and "
                    "sometimes states a general present reality. Read the strength of the "
                    "condition from context rather than from the form.",
        "example_ref": "Matt 9:21; 1 Cor 13:1-3; 1 John 1:7, 9",
    },

    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.manner_means.articular_infinitive": {
        "formation": "ἐν τῷ followed by an infinitive.",
        "function": "Says how the controlling verb's action was carried out. Render with "
                    "'by ... -ing'.",
        "example_ref": "Acts 3:26",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.manner_means.adverbial_participle": {
        "formation": "Anarthrous participle matching its subject in case, number and gender.",
        "function": "Answers 'How?'. Manner describes the attitude or emotion the action was "
                    "done with; means names the instrument or method that accomplished it. The "
                    "two are close and often hard to separate.",
        "example_ref": "Acts 16:16",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.manner_means.relative_pn_hon": {
        "formation": "A clause headed by the relative pronoun ὅν.",
        "function": "The relative clause names the manner or means of the main verb's action.",
        "example_ref": "Acts 1:11",
    },

    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.purpose.infinitive": {
        "formation": "A bare infinitive, or τοῦ, εἰς τό or πρὸς τό followed by an infinitive.",
        "function": "Names the goal the controlling verb aims at. Render with 'to', 'in order "
                    "to' or 'for the purpose of'.",
        "example_ref": "1 Tim 1:15",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.purpose.adverbial_participle": {
        "formation": "Anarthrous participle matching its subject; it normally follows the main "
                     "verb rather than preceding it.",
        "function": "States the intent behind the finite verb's action. Render it like an "
                    "infinitive, or with 'with the purpose of'.",
        "example_ref": "1 Cor 4:14",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.purpose.hina_subjunctive": {
        "formation": "ἵνα plus the subjunctive. ὅπως does the same work; for a negative purpose "
                     "use μήπως, μήπου or μήποτε.",
        "function": "States what the controlling verb intends to bring about. Render with 'in "
                    "order that' or 'so that'.",
        "example_ref": "1 Pet 3:18",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.purpose.relative_pn_hoitines": {
        "formation": "A clause headed by the relative pronoun οἵτινες.",
        "function": "The relative clause names the purpose of the main verb's action.",
        "example_ref": "Matt 21:41",
    },

    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.resultative.infinitive": {
        "formation": "ὥστε followed by an infinitive, or a bare infinitive, or τοῦ or εἰς τό "
                     "followed by an infinitive.",
        "function": "States the outcome the controlling verb produced, with the weight on the "
                    "effect itself - whether or not it was intended. Render with 'so that', "
                    "'so as to' or 'with the result that'.",
        "example_ref": "Gal 5:7",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.resultative.adverbial_participle": {
        "formation": "Anarthrous participle matching its subject; it follows the main verb.",
        "function": "Names what actually came of the main verb's action. The result may be "
                    "logical or it may be something that followed in time.",
        "example_ref": "John 5:18",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.resultative.hina_subjunctive": {
        "formation": "ἵνα plus the subjunctive. ὥστε, ὡς and ὅτι also head result clauses.",
        "function": "States a consequence of the verbal action that was not aimed at. This is "
                    "what separates it from a purpose ἵνα clause, which is identical in form.",
        "example_ref": "Rom 11:11",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.resultative.relative_adverb_hothen": {
        "formation": "A clause headed by the relative adverb ὅθεν.",
        "function": "The relative clause names the result of the main verb's action.",
        "example_ref": "Heb 8:3",
    },

    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.time.articular_infinitive": {
        "formation": "μετὰ τό plus infinitive for action before the main verb; ἐν τῷ plus "
                     "infinitive for action alongside it; πρὸ τοῦ, πρίν or πρὶν ἤ plus "
                     "infinitive for action after it.",
        "function": "Places the main verb's action in time. Render with 'after', 'while / as / "
                    "when', or 'before' plus a finite verb, according to the preposition used.",
        "example_ref": "Matt 6:8",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.time.adverbial_participle": {
        "formation": "Anarthrous participle matching its subject in case, number and gender.",
        "function": "Answers 'When?'. The participle's action may fall before the main verb "
                    "('after doing'), alongside it ('while doing'), or after it ('before doing').",
        "example_ref": "Matt 21:18, 23",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.time.hote_indicative": {
        "formation": "ὅτε plus the indicative. ὅταν ('whenever') is the indefinite counterpart "
                     "and normally takes the subjunctive instead.",
        "function": "Fixes when the main clause's action took place.",
        "example_ref": "Matt 19:1",
        "note": "This is the 'when' branch, which sits ahead of the main clause. Clauses headed "
                "by ἕως or ἄχρι ('until') do the opposite and follow it - see the `time` split "
                "flagged in JSON_skeleton.",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.time.relative_pn": {
        "formation": "A relative pronoun clause, usually with a preposition attached - ἀφʼ ἧς, "
                     "ἐν ᾧ.",
        "function": "The relative clause fixes the time of the main verb's action.",
        "example_ref": "Col 1:9; Mark 2:19",
    },

    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.comparative.adverbial_participle": {
        "formation": "Anarthrous participle matching its subject in case, number and gender.",
        "function": "Draws an analogy between the participle's action and the main verb's.",
        "example_ref": None,
        "note": "Unattested. The reference taxonomy builds comparison only from conjunctive and "
                "relative clauses, with no participial or infinitival option. Retained because "
                "the skeleton lists it, but nothing in the sources backs it.",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.comparative.kathos_hos_indicative": {
        "formation": "καθώς plus the indicative. καθάπερ, οὕτως, ὡς and ὡσαύτως head the same "
                     "kind of clause, as does the relative adjective ὅσος.",
        "function": "Sets one idea alongside another as an analogy, or says how something was "
                    "done. Render with 'as', 'just as', 'in the same way' or 'thus'.",
        "example_ref": "Eph 4:32",
    },

    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.local.hopou_indicative": {
        "formation": "A clause headed by the relative adverb ὅπου.",
        "function": "Gives the place, or metaphorically the sphere, in which the action happens. "
                    "Render with 'where' or 'the place which'.",
        "example_ref": "Mark 4:5",
    },
    "sentence_construction_possibilitites.main_and_dependent_sentence.adverbial.local.relative_adverb_hou": {
        "formation": "οὗ plus the indicative. ὅθεν ('from where') is the other local relative "
                     "adverb.",
        "function": "Locates the main verb's action in space or in a figurative sphere.",
        "example_ref": "Rom 4:15",
        "note": "The sources pair these the other way round - οὗ takes the indicative and ὅπου "
                "is the relative adverb. Either way the two keys cover the same pair.",
    },

    # ---- substantival dependent clause ----------------------------------------------------

    "sentence_construction_possibilitites.main_and_dependent_sentence.substantival": {
        "formation": "An infinitival, participial, conjunctive (ἵνα or ὅτι) or relative clause "
                     "standing where a noun would.",
        "function": "The whole clause behaves as a noun and can occupy any slot a noun could - "
                    "subject, predicate nominative, direct object, indirect discourse, or "
                    "apposition.",
        "example_ref": None,
    },

    # ---- relative sentence ----------------------------------------------------------------

    "sentence_construction_possibilitites.main_and_relative_sentence.substantival.indicative.subject": {
        "formation": "ὅ plus the indicative, with no antecedent, standing in the subject slot of "
                     "the main verb.",
        "function": "The relative clause serves as the subject of the main verb.",
        "example_ref": "Matt 13:12",
    },
    "sentence_construction_possibilitites.main_and_relative_sentence.substantival.indicative.object": {
        "formation": "ὅ plus the indicative, standing in the object slot. The pronoun takes its "
                     "case from its job inside its own clause, not from the slot it fills "
                     "outside it.",
        "function": "The relative clause serves as the direct object of the main verb.",
        "example_ref": "Luke 11:6",
    },
    "sentence_construction_possibilitites.main_and_relative_sentence.substantival.indicative.independent": {
        "formation": "A definite relative clause: relative pronoun plus a verb in the "
                     "indicative. The pronoun agrees with its antecedent in number and gender, "
                     "but takes its case from its function inside the relative clause.",
        "function": "Points back to something specific already in the sentence - a particular "
                    "person, group, fact, event or action.",
        "example_ref": "Mark 10:29",
    },
    "sentence_construction_possibilitites.main_and_relative_sentence.substantival.subjunctive": {
        "formation": "An indefinite relative clause: ὅστις with ἄν or ἐάν, or ὅς (δʼ) ἄν, plus "
                     "the subjunctive.",
        "function": "Points to an unspecified person, group, event or action - 'whoever', "
                    "'whatever'. There is no antecedent. Translate as though it were indicative: "
                    "the uncertainty is about who, not about whether.",
        "example_ref": "Matt 20:4, 27",
    },
    "sentence_construction_possibilitites.main_and_relative_sentence.adjectival": {
        "formation": "Relative pronoun agreeing with its antecedent in number and gender, its "
                     "case set by its role inside the relative clause. It follows its referent.",
        "function": "Attributive only - it describes, explains or narrows the substantive it "
                    "attaches to.",
        "example_ref": "Eph 6:17; 1 John 2:7",
    },

    # ---- coordination ----------------------------------------------------------------------

    "sentence_construction_possibilitites.two_complete_coordinating_sentence.connector_piece": {
        "formation": "A coordinating conjunction between two independent clauses. Connective: "
                     "καί, δέ. Contrastive: ἀλλά, δέ, πλήν. Correlative: μέν … δέ, καί … καί. "
                     "Inferential: οὖν, ἄρα, διό. Explanatory: γάρ. Disjunctive: ἤ.",
        "function": "Carries the movement of thought from one clause to the next by naming the "
                    "logical relation between them. Both clauses stay independent.",
        "example_ref": None,
        "note": "γάρ, δέ, οὖν and μέν are postpositive and cannot stand first in their clause. "
                "See word_order.hard_constraints in JSON_skeleton.",
    },

    "sentence_construction_possibilitites.simple_beginner_sentence": {
        "formation": "A single independent clause: nominative subject, finite verb, and an "
                     "accusative direct object if the verb is transitive.",
        "function": "One unsubordinated assertion. Unmarked order is subject, then predicate, "
                    "then complement.",
        "example_ref": None,
    },

    # ---- sentence vitals: verb --------------------------------------------------------------

    "sentence_vitals.verb.finite_verb": {
        "formation": "A verb inflected for person and number, in the indicative, subjunctive, "
                     "optative or imperative.",
        "function": "Carries the predicate. A Greek verb form packs aspect, mood and voice "
                    "together with person and number, so the verb alone can stand as a complete "
                    "clause without a separate subject word.",
        "example_ref": None,
    },
    "sentence_vitals.verb.finite_with_infinitive_complement": {
        "formation": "A finite helper verb followed by a complementary infinitive. The usual "
                     "helpers are ἄρχομαι, βούλομαι, δύναμαι, ἐπιτρέπω, ζητέω, θέλω, μέλλω and "
                     "ὀφείλω.",
        "function": "The infinitive finishes a thought the helper verb cannot finish on its "
                    "own. These helpers seldom appear without one.",
        "example_ref": None,
    },

    # ---- sentence vitals: subject -----------------------------------------------------------

    "sentence_vitals.subject.nominative": {
        "formation": "A substantive in the nominative, agreeing with the finite verb in person "
                     "and number.",
        "function": "The subject of a finite verb.",
        "example_ref": None,
        "note": "Agreement has regular exceptions: a neuter plural subject usually takes a "
                "singular verb, a collective singular may take a plural verb, and a compound "
                "subject may take a singular verb agreeing with whichever part is named first.",
    },
    "sentence_vitals.subject.substantival_participle": {
        "formation": "A participle, normally with the article and with no noun for it to "
                     "modify. The article fixes its case - nominative when it is the subject.",
        "function": "Stands where a noun would and can do nearly anything a noun can do. Render "
                    "with 'the one who' or 'the thing which'. Verbal aspect is usually still "
                    "felt.",
        "example_ref": "John 3:18",
    },
    "sentence_vitals.subject.hoti_indicative": {
        "formation": "ὅτι plus the indicative, the whole clause occupying the subject slot.",
        "function": "The clause serves as the subject of the main verb.",
        "example_ref": "Gal 3:11",
    },
    "sentence_vitals.subject.hina_subjunctive": {
        "formation": "ἵνα plus the subjunctive, the whole clause occupying the subject slot.",
        "function": "A substantival ἵνα clause doing the work of a subject rather than "
                    "expressing purpose.",
        "example_ref": "1 Cor 4:2",
    },
    "sentence_vitals.subject.relative_pn_ho": {
        "formation": "A clause headed by ὅ with no antecedent.",
        "function": "The relative clause serves as the subject of the main verb.",
        "example_ref": "Matt 13:12",
    },

    # ---- sentence vitals: object ------------------------------------------------------------

    "sentence_vitals.object.accusative": {
        "formation": "A substantive in the accusative following a transitive verb.",
        "function": "Receives the action of the verb directly, and in doing so limits its scope.",
        "example_ref": None,
        "note": "The case is chosen by the verb, not by the role. Verbs of sensation, emotion "
                "and volition, sharing and ruling take a genitive object; verbs of worship, "
                "service, obedience and belief take a dative one.",
    },
    "sentence_vitals.object.substantival_participle": {
        "formation": "A participle, normally articular, with no noun for it to modify; "
                     "accusative when it is the direct object.",
        "function": "Stands where a noun would in the object slot.",
        "example_ref": "Phil 3:17",
    },
    "sentence_vitals.object.relative_clause": {
        "formation": "ὅ plus a verb, the whole clause occupying the object slot. The pronoun's "
                     "case comes from its job inside its own clause.",
        "function": "The relative clause serves as the direct object of the main verb.",
        "example_ref": "Luke 11:6",
    },
    "sentence_vitals.object.substantival_infinitive": {
        "formation": "A bare or articular infinitive in the object slot, after a verb that is "
                     "not one of perceiving or speaking.",
        "function": "The direct object of the finite verb.",
        "example_ref": "1 Tim 2:8",
        "note": "After a verb of perceiving or speaking the same construction becomes indirect "
                "discourse - a specialised direct object standing in for a finite verb of the "
                "original speech.",
    },
    "sentence_vitals.object.hoti_indicative": {
        "formation": "ὅτι plus the indicative, the whole clause occupying the object slot.",
        "function": "Serves as the direct object. After an ordinary transitive verb it is a "
                    "plain object clause; after a verb of perceiving or speaking it reports "
                    "speech or thought and is rendered with 'that'.",
        "example_ref": "John 3:33",
    },
    "sentence_vitals.object.hina_subjunctive": {
        "formation": "ἵνα plus the subjunctive, the whole clause occupying the object slot.",
        "function": "A content clause - it answers 'What?' rather than 'Why?', which is the "
                    "only thing separating it from a purpose ἵνα clause of identical shape.",
        "example_ref": "Matt 12:16",
    },

    # ---- supplementary pieces ----------------------------------------------------------------

    "other_supplementary_pieces.extra_case_usage.genitive": {
        "formation": "A substantive in the genitive, normally placed after the noun it "
                     "qualifies.",
        "function": "Qualifies, and occasionally separates. It attaches to a head term and "
                    "narrows it - saying what kind, whose, from what source, or in what respect.",
        "example_ref": None,
    },
    "other_supplementary_pieces.extra_case_usage.dative": {
        "formation": "A substantive in the dative, tied to the verb rather than to a noun.",
        "function": "Covers personal interest, reference, position and means.",
        "example_ref": None,
    },
    "other_supplementary_pieces.adverbial.verbal_modification_proper": {
        "formation": "An adverb, normally uninflected; -ως is the commonest ending. It rarely "
                     "stands between a verb and its object, so place it on one side or the "
                     "other.",
        "function": "Modifies the verb - describes the action or says how it was carried out.",
        "example_ref": None,
    },
    "other_supplementary_pieces.adverbial.substantival_modification": {
        "formation": "An adverb turned into a substantive by the article, or one attached to an "
                     "adjective or another adverb.",
        "function": "Modifies something other than the verb. The article can convert an adverb "
                    "into a noun outright.",
        "example_ref": None,
    },
    "other_supplementary_pieces.prepositions": {
        "formation": "A preposition followed by a substantive in whichever case that preposition "
                     "governs. The object almost always comes after the preposition; χάριν, "
                     "χωρίς and ἕνεκα are the rare exceptions.",
        "function": "Makes explicit the relation a substantive has to the rest of the clause - "
                    "work the case alone would otherwise have to carry. A preposition may govern "
                    "one, two or three cases, meaning something different with each.",
        "example_ref": None,
    },
    "other_supplementary_pieces.particles": {
        "formation": "Indeclinable words. Several are postpositive - ἄν, γάρ, δέ, γέ, μέν, οὖν - "
                     "and cannot open their clause.",
        "function": "Connect, qualify, intensify or negate. For negation, οὐ and its compounds "
                    "go with the indicative and μή and its compounds elsewhere; οὐ μή with the "
                    "aorist subjunctive is emphatic denial.",
        "example_ref": None,
    },
}

# Plan run

**3 cards, $0.571, 109s of generation.**


## grammar

### `article::ὁ::nominative.masculine.singular`

**ὁ ἔσχατος ἐλθὼν οὐδὲ ἕνα ἄρτον εὗρεν.**

*The last one, when he arrived, found not even one loaf of bread.* - target `ὁ`

- shape: a single main clause
- extra, one of: -
- setting: s191 - The last traveller to arrive finds no food left.
- attempts: 1, 16.0s, $0.1506
- unknown words glossed: -

  - attempt 1: 16.0s, 1541 output tokens

| word | given as | GNT check |
|---|---|---|
| ὁ | nominative masculine singular of ὁ | confirmed |
| ἔσχατος | nominative masculine singular of ἔσχατος | confirmed |
| ἐλθὼν | aorist active participle nominative masculine singular of ἔρχομαι | confirmed |
| οὐδὲ | adverb of οὐδέ | confirmed |
| ἕνα | accusative masculine singular of εἷς | confirmed |
| ἄρτον | accusative masculine singular of ἄρτος | confirmed |
| εὗρεν | aorist active indicative 3rd person singular of εὑρίσκω | confirmed |

<details><summary>reasoning</summary>

The sentence carries no other article form, so ὁ has nothing to compete with. Without it, ἔσχατος could be read as a predicate ('he came last'). With ὁ it becomes the substantive subject, 'the last one', which frames the whole scene. The fronted οὐδὲ ἕνα ἄρτον gives the late arrival his rhetorical sting inside a single main clause with one temporal participle.

</details>

## vocabulary

### `βαπτίζω`

**ἐὰν ὁ δοῦλος ἔλθῃ ἐκ τοῦ ἀγροῦ, βαπτισθήτω ὕδατι· ἐγγίζει γὰρ τὸ σάββατον.**

*If the servant comes in from the field, let him wash himself with water, for the Sabbath is drawing near.* - target `βαπτισθήτω`

- shape: a main clause with an adverbial dependent clause: conditional, third class
- extra, one of: Abstract (i.e., the Article with Abstract Nouns) | Ἐκ (Genitive) | Possessive Genitive
- setting: adapted:s072 - A household makes ready for the Sabbath at sunset and the lamp oil runs out.
- attempts: 1, 53.8s, $0.2159
- unknown words glossed: -

  - attempt 1: 53.8s, 4750 output tokens

| word | given as | GNT check |
|---|---|---|
| ἐὰν | conjunction of ἐάν | confirmed |
| ὁ | nominative masculine singular of ὁ | confirmed |
| δοῦλος | nominative masculine singular of δοῦλος | confirmed |
| ἔλθῃ | aorist active subjunctive 3rd person singular of ἔρχομαι | confirmed |
| ἐκ | preposition of ἐκ | confirmed |
| τοῦ | genitive masculine singular of ὁ | confirmed |
| ἀγροῦ | genitive masculine singular of ἀγρός | confirmed |
| βαπτισθήτω | aorist passive imperative 3rd person singular of βαπτίζω | confirmed |
| ὕδατι | dative neuter singular of ὕδωρ | confirmed |
| ἐγγίζει | present active indicative 3rd person singular of ἐγγίζω | confirmed |
| γὰρ | conjunction of γάρ | confirmed |
| τὸ | nominative neuter singular of ὁ | confirmed |
| σάββατον | nominative neuter singular of σάββατον | confirmed |

<details><summary>reasoning</summary>

The card uses the attested washing sense of βαπτίζω (53.31) rather than the rite. A servant who comes in from the field, with water named as the means and the Sabbath at hand, points the student to cleansing and shuts out 'baptize'. The Sabbath-eve household fits this sense naturally and keeps the card clear of baptismal episodes. Mark 7:4's market-and-eating frame is avoided by giving no meal and ending on a γάρ clause about the approaching Sabbath. Protasis ἐάν + aorist subjunctive, apodosis attested βαπτισθήτω, ἐκ + genitive as the texture.

</details>

## syntax

### `genitive/adjectival/descriptive-genitive`

**ὁ ἰατρὸς εἶπεν τῷ ἀνδρί· Πεσὼν ἀπὸ τῆς θύρας τῶν προβάτων, μεῖνον ἐν τῷ οἴκῳ ἑπτὰ ἡμέρας.**

*The physician said to the man: 'Because you fell from the sheep gate, stay in the house seven days.'* - target `τῶν προβάτων`

- shape: a main clause with an adverbial dependent clause: causal, adverbial participle
- extra, one of: Well-Known (“Celebrity” or “Familiar” Article) | Aorist Imperative | Instantaneous Present (a.k.a. Aoristic or Punctiliar Present)
- setting: adapted:s021 - A physician sets the broken arm of a stonemason who fell from scaffolding.
- attempts: 1, 38.9s, $0.2044
- unknown words glossed: {'ἰατρός': 'physician'}

  - attempt 1: 38.9s, 3878 output tokens

| word | given as | GNT check |
|---|---|---|
| ὁ | nominative masculine singular of ὁ | confirmed |
| ἰατρὸς | nominative masculine singular of ἰατρός | confirmed |
| εἶπεν | aorist active indicative 3rd person singular of λέγω | confirmed |
| τῷ | dative masculine singular of ὁ | confirmed |
| ἀνδρί | dative masculine singular of ἀνήρ | confirmed |
| Πεσὼν | aorist active participle nominative masculine singular of πίπτω | confirmed |
| ἀπὸ | preposition of ἀπό | confirmed |
| τῆς | genitive feminine singular of ὁ | confirmed |
| θύρας | genitive feminine singular of θύρα | confirmed |
| τῶν | genitive neuter plural of ὁ | confirmed |
| προβάτων | genitive neuter plural of πρόβατον | confirmed |
| μεῖνον | aorist active imperative 2nd person singular of μένω | confirmed |
| ἐν | preposition of ἐν | confirmed |
| τῷ | dative masculine singular of ὁ | confirmed |
| οἴκῳ | dative masculine singular of οἶκος | confirmed |
| ἑπτὰ | adjective (indeclinable numeral) of ἑπτά | confirmed |
| ἡμέρας | accusative feminine plural of ἡμέρα | confirmed |

<details><summary>reasoning</summary>

This is a generic usage, the default genitive, so I did not force out every neighbour. In τῆς θύρας τῶν προβάτων the head is not a verbal noun, the sheep do not own the gate, the gate is not part of them, and no adjective can replace the genitive. The natural sense is 'the gate having to do with sheep'. I used the θύρα/πρόβατον set in an adapted s021 scene: a mason's fall from a stone gateway gives the physician's aorist imperative (μεῖνον) its reason through the fronted causal participle. It shares only the two-word phrase with John 10, with no shepherd imagery.

</details>

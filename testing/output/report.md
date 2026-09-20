# Card test run

## Spend

| category | stage | calls | output tokens | cost |
|---|---|---|---|---|
| syntax | audited | 1 | 2,440 | $0.031 |
| syntax | generated | 1 | 4,304 | $0.057 |
| **all** | | **2** | **6,744** | **$0.088** |

$0.0442 per call.

## syntax

Card type: `function_recall_syntax_g2e` · 1 generated, 1 audited

| verdict | count |
|---|---|
| revise | 1 |

### `genitive/adjectival/descriptive-genitive`

> Εἰσῆλθον εἰς οἰκίαν θανάτου καὶ εἶδον ἐκεῖ πολλοὺς νεκρούς.

*I entered a house of death and saw many dead people there.*

**target:** θανάτου  
**verdict:** revise
  — The card is grammatically fine and level-appropriate, but the reasoning's central claim — that οἰκία θανάτου resists attributive-adjective conversion — is not actually true ('deathly house' works fine), so the example doesn't cleanly isolate descriptive from attributive genitive; the generator should pick a genitive noun/phrase where the adjective conversion genuinely fails (e.g. an abstract noun with no natural adjective) or justify why 'deathly' doesn't count as a valid conversion.

**blind reading recalled Ezekiel 37:1-2 (LXX vision of the valley of dry bones)** — The clause 'εἶδον ἐκεῖ πολλοὺς νεκρούς' (I saw many dead there) evokes the prophetic vision of a place filled with the dead, even though no wording is shared.

**findings**

- **constraint 7** — The reasoning claims οἰκία θανάτου 'resists smooth one-word adjective conversion,' but 'house of death' converts naturally to 'deathly house' or 'house of the dead,' which is exactly the attributive-genitive test the sibling category uses. This leaves the descriptive/attributive distinction ambiguous rather than clearly demonstrated.
- **echo / scene** (Ezekiel 37:1-2) — Entering a place and seeing 'many dead' faintly recalls the valley-of-bones vision; not disqualifying but worth noting since it colors the reader's first impression.
- **echo / collocation** — οἰκία θανάτου is not an attested biblical collocation (unlike πύλαι θανάτου, 'gates of death,' Job 38:17), so the phrase reads as invented rather than idiomatic — acceptable for a drill sentence, but it weakens the pedagogical force of treating it as a natural descriptive genitive.
- **reasoning** — The reasoning asserts that οἰκία θανάτου 'resists smooth one-word adjective conversion (ruling out attributive)' but does not actually perform this swap test — 'house of death' converts easily to 'deathly house,' which is precisely the kind of conversion that would mark it attributive rather than descriptive. The claim is asserted, not demonstrated, and is arguably false as stated.

<details><summary>reasoning</summary>

Descriptive genitive is the broad 'characterized by' catch-all, best shown with an abstract genitive noun that resists smooth one-word adjective conversion (ruling out attributive) and lacks any fullness, material, possession, or partitive sense. Using οἰκία θανάτου ('house of death') gives a vivid scene where the genitive plainly characterizes the house without being 'belonging to,' 'made of,' 'full of,' or a same-referent apposition. The surrounding clause stays simple past-tense narration so nothing but the genitive phrase demands parsing.

</details>

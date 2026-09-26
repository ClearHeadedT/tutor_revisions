from llm_calls.main import llm_call_card_formation
from greek_text import normalize_greek
from data.student_data.student_data_helper_functions import load_vocabulary_senses
from tasks.card_randomization.card_randomize_utils import build_sentence_plan
from tasks.new_card_creation.utils import(
    card_instructions_loader,
    parse_card_reply,
    enrich_vocabulary_senses,
    unpack_grammatical_item,
    unpack_syntactic_item
)
from tasks.new_card_creation.prefetch import lexical_profile
from tasks.new_card_creation.verify import check_card

# How many times a card that fails its checks is sent back before it is kept as it stands.
CHECK_RETRIES = 2


def form_checked_card(instructions, card_content, student, target=None, target_features=None,
                      target_forms=None, target_lexemes=None, keep_replies=False):
    """One card from the model, run through the deterministic checks in verify.py and sent back
    with their findings up to CHECK_RETRIES times.

    A card that still fails is kept, with its findings recorded under "check", rather than
    dropped: a card silently lost is harder to learn from than one marked for a look. "helps"
    carries the glosses for the one or two unknown words a passing card is allowed. Every attempt
    is logged with its time and tokens; keep_replies adds the raw reply to each, for testing."""
    rejected, attempts = [], []
    while True:
        reply, usage = llm_call_card_formation(instructions, card_content, rejected)
        try:
            card = parse_card_reply(reply)
            check = check_card(card, student, target, target_features, target_forms, target_lexemes)
        except ValueError:
            card, check = {}, {"findings": ["The reply was not a single JSON object in the format asked "
                                            "for. Return the card as one JSON object in a ```json fence."],
                               "notes": [], "helps": None, "words": []}
        attempts.append({**usage, "findings": check["findings"], **({"reply": reply} if keep_replies else {})})
        if not check["findings"] or len(rejected) == CHECK_RETRIES:
            break
        rejected.append((reply, check["findings"]))
    return {**card, "helps": check["helps"],
            "check": {"findings": check["findings"], "notes": check["notes"], "words": check["words"],
                      "attempts": attempts,
                      "seconds": round(sum(a["seconds"] for a in attempts), 1)}}


class NewVocabularyCard:
    """Everything known about one lexical form, gathered from Text-Fabric and
    Louw-Nida, ready to be written into austin's vocabulary scaffolding.
    Review cards are not handled here -- this only builds the scaffolding."""

    def __init__(self, lexeme, student):
        """lexeme is a (form, lexical_entry) pair. Takes the word's entry from the shared
        senses file, enriching it from Text-Fabric and Louw-Nida if it is not there yet.
        The entry holds the conventional lexicon form, the Text-Fabric lexical facts,
        and the Louw-Nida sense breakdown. The student is who the card gets written for."""
        self.student = student
        self.lemma = normalize_greek(lexeme[0])
        senses = load_vocabulary_senses()
        if self.lemma not in senses:
            senses = enrich_vocabulary_senses([lexeme])
        entry = senses[self.lemma]
        self.lexical_entry = entry["lexical_entry"]
        self.tf_lexical_info = entry["tf_lexical_info"]
        self.ln_sense_info = entry["ln_sense_info"] or {}

    def generate_vocabulary_card(self, desired_card_type: str):
        """Produces vocabulary card through LLM call, contingent on desired type"""
        instructions = card_instructions_loader(desired_card_type)
        card_content = {
            "item": self.vocabulary_entry(),
            "recent_generations": self.student.recent_generations(self.lemma),
            "student": self.student.student_overview(),
            "sentence_plan": build_sentence_plan(self.student, desired_card_type, "vocabulary", self.lemma),
        }
        card = form_checked_card(instructions, card_content, self.student, target=self.lemma)
        return {"card_type": desired_card_type, **card}

    def vocabulary_entry(self):
        entry = {
            **self.tf_lexical_info,
            "lexical_entry": self.lexical_entry,
            "summary": self.ln_sense_info.get("summary"),
        }
        usage = lexical_profile(self.lemma)
        if usage:
            entry["attested_usage"] = usage
        return entry

    def senses_entry(self):
        return {
            "primary_sense": self.ln_sense_info.get("primary_sense"),
            "secondary_senses": self.ln_sense_info.get("secondary_senses", []),
        }


class NewGrammarCard:
    """Everything known about a grammatical concept, derived from 
    the grammar scaffolding JSON for first card formulation.
    Currently wired for text_recall_grammar_g2e and cloze_grammar_e2g cards"""
    def __init__(self, grammar_item_key, student):
        """grammar_item_key is a slot key such as decl2::n-2a::genitive.singular. The
        slot is unpacked into the three levels the card reasons from: the slot itself,
        the rule it belongs to, and the pattern whose chart it fills."""
        self.student = student
        self.key = grammar_item_key
        unpacked = unpack_grammatical_item(grammar_item_key)
        self.item = unpacked["item"]
        self.rule = unpacked["rule"]
        self.pattern = unpacked["pattern"]


    def generate_grammar_card(self, desired_card_type):
        """Produces grammar card through LLM call, contingent on desired type"""
        instructions = card_instructions_loader(desired_card_type=desired_card_type)
        card_content = {
            "item": self.grammar_entry(),
            "recent_generations": self.student.recent_generations(self.key),
            "student": self.student.student_overview(),
            "sentence_plan": build_sentence_plan(self.student, desired_card_type, "grammar", self.key),
        }
        card = form_checked_card(instructions, card_content, self.student,
                                 target_features=self.item.get("features"),
                                 target_forms=[form["form"] for form in self.item["gnt_forms"]])
        return {"card_type": desired_card_type, **card}


    def grammar_entry(self):
        return {"item": self.item, "rule": self.rule, "pattern": self.pattern}


class NewSyntaxCard:
    """Everything known about a syntactic usage, derived from
    the syntax scaffolding JSON for first card formulation.
    Currently wired for function_recall_syntax_g2e and self_formulation_syntax_e2g cards"""
    def __init__(self, syntax_item_key, student):
        """syntax_item_key is a path such as dative/pure-dative-uses/dative-indirect-object.
        The usage is unpacked into the three levels the card reasons from: the usage itself,
        the categories it sits under, and the usages filed beside it."""
        self.student = student
        self.key = syntax_item_key
        unpacked = unpack_syntactic_item(syntax_item_key)
        self.item = unpacked["item"]
        self.ancestors = unpacked["ancestors"]
        self.sibling_usages = unpacked["sibling_usages"]


    def generate_syntax_card(self, desired_card_type):
        """Produces syntax card through LLM call, contingent on desired type"""
        instructions = card_instructions_loader(desired_card_type=desired_card_type)
        card_content = {
            "item": self.syntax_entry(),
            "recent_generations": self.student.recent_generations(self.key),
            "student": self.student.student_overview(),
            "sentence_plan": build_sentence_plan(self.student, desired_card_type, "syntax", self.key),
        }
        card = form_checked_card(instructions, card_content, self.student,
                                 target_lexemes=self.item.get("gnt_lexemes"))
        return {"card_type": desired_card_type, **card}


    def syntax_entry(self):
        return {"item": self.item, "ancestors": self.ancestors, "sibling_usages": self.sibling_usages}








class AustinNewVocabularyCard(NewVocabularyCard):
    """NOT for forming review cards from existing cards
    Forms entirely NEW cards and adds them to austin_scaffolding"""
    def __init__(self, lexical_form):
        super().__init__(lexical_form)


    def generate_initial_vocabulary(self, lemma):
        easy_instructions = card_instructions_loader(desired_card_type="text_recall_grammar_g2e")
        intermediate_instruction = card_instructions_loader(desired_card_type="text_recall_grammar_g2e")
        
        









# def generate_initial_grammar(self):
#     easy_instructions = card_instructions_loader(desired_card_type="text_recall_grammar_g2e")
#     intermediate_instructions = card_instructions_loader(desired_card_type="cloze_grammar_e2g")
#     raise NotImplementedError



# def generate_initial_syntax(self):
#     easy_instructons = card_instructions_loader(desired_card_type="function_recall_syntax_g2e")
#     intermediate_instructions = card_instructions_loader(desired_card_type="self_formulation_syntax_e2g")
#     raise NotImplementedError



# def austin_scaffolding_save(self):
#     """Writes to both files under the same lemma key, which is what links them."""
#     lemma = self.tf_lexical_info["lemma"]
#     scaffolding = load_austin_vocabulary_scaffolding()
#     scaffolding["vocabulary"][lemma] = self.vocabulary_entry()
#     save_austin_vocabulary_scaffolding(scaffolding)

#     senses = load_austin_vocabulary_senses()
#     senses["senses"][lemma] = self.senses_entry()
#     save_austin_vocabulary_senses(senses)

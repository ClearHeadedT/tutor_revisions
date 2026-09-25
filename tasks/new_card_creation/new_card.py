from llm_calls.main import llm_call_card_formation
from greek_text import normalize_greek
from data.student_data.student_data_helper_functions import load_vocabulary_senses
from tasks.card_randomization.card_randomize_utils import build_sentence_plan
from tasks.new_card_creation.utils import(
    card_instructions_loader,
    parse_card_reply,
    enrich_vocabulary_senses,
    unpack_grammatical_item
)
from tasks.new_card_creation.verify import check_card

# How many times a card that fails its checks is sent back before it is kept as it stands.
CHECK_RETRIES = 2


def form_checked_card(instructions, card_content, student, target=None):
    """One card from the model, run through the deterministic checks in verify.py and sent back
    with their findings up to CHECK_RETRIES times.

    A card that still fails is kept, with its findings recorded under "check", rather than
    dropped: a card silently lost is harder to learn from than one marked for a look. "helps"
    carries the glosses for the one or two unknown words a passing card is allowed."""
    rejected = []
    while True:
        reply = llm_call_card_formation(instructions, card_content, rejected)
        card = parse_card_reply(reply)
        check = check_card(card, student, target)
        if not check["findings"] or len(rejected) == CHECK_RETRIES:
            break
        rejected.append((reply, check["findings"]))
    return {**card, "helps": check["helps"],
            "check": {"findings": check["findings"], "overlap": check["overlap"],
                      "attempts": len(rejected) + 1}}



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
        return {
            **self.tf_lexical_info,
            "lexical_entry": self.lexical_entry,
            "summary": self.ln_sense_info.get("summary"),
        }

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
        """grammar_item_key is a slot key such as decl2::λόγος::genitive.singular. The
        slot is unpacked into the three levels the card reasons from: the slot itself,
        the rule it belongs to, and the paradigm whose chart it fills."""
        self.student = student
        self.key = grammar_item_key
        unpacked = unpack_grammatical_item(grammar_item_key)
        self.item = unpacked["item"]
        self.rule = unpacked["rule"]
        self.paradigm = unpacked["paradigm"]


    def generate_grammar_card(self, desired_card_type):
        """Produces grammar card through LLM call, contingent on desired type"""
        instructions = card_instructions_loader(desired_card_type=desired_card_type)
        card_content = {
            "item": self.grammar_entry(),
            "recent_generations": self.student.recent_generations(self.key),
            "student": self.student.student_overview(),
            "sentence_plan": build_sentence_plan(self.student, desired_card_type, "grammar", self.key),
        }
        card = form_checked_card(instructions, card_content, self.student)
        return {"card_type": desired_card_type, **card}


    def grammar_entry(self):
        return {"item": self.item, "rule": self.rule, "paradigm": self.paradigm}

    






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

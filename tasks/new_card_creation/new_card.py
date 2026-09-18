from llm_calls.main import llm_call_card_formation
from tasks.new_card_creation.utils import(
    card_instructions_loader,
    parse_card_reply,
)



class NewVocabularyCard:
    """Everything known about one lexical form, gathered from Text-Fabric and
    Louw-Nida, ready to be written into austin's vocabulary scaffolding.
    Review cards are not handled here -- this only builds the scaffolding."""

    def __init__(self, lemma, senses):
        """Reads one lemma out of the shared enrichment cache, which the cache builder
        fills from Text-Fabric in advance. Each entry carries the conventional lexicon
        form, the Text-Fabric lexical facts, and the Louw-Nida sense breakdown."""
        entry = senses[lemma]
        self.lexical_entry = entry["lexical_entry"]
        self.tf_lexical_info = entry["tf_lexical_info"]
        self.ln_sense_info = entry["ln_sense_info"] or {}

    def generate_vocabulary_card(self, desired_card_type: str, student_overview):
        """Produces vocabulary card through LLM call, contingent on desired type"""
        instructions = card_instructions_loader(desired_card_type)
        card_content = {
            "item": self.vocabulary_entry(),
            "recent_generations": [],
            "student": student_overview,
        }
        llm_call = llm_call_card_formation(
            llm_instructions=instructions,
            card_content=card_content,
        )
        return {"card_type": desired_card_type, **parse_card_reply(llm_call)}

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

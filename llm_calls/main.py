from llm_calls.client import make_client
from llm_calls.llm_constants import CARD_MODEL, MAX_TOKENS
import json


def llm_call_card_formation(llm_instructions, card_content):
    """card_content is the dict instructions_cap describes to the model: "item",
    "recent_generations", and "student". It is serialized here rather than retyped
    into a sentence, and ensure_ascii keeps the Greek readable in the prompt."""
    client = make_client()
    response = client.messages.create(
        model=CARD_MODEL,
        max_tokens=MAX_TOKENS,
        system=llm_instructions,
        messages=[{"role": "user", "content": json.dumps(card_content, indent=2, ensure_ascii=False)}],
    )
    return next(block.text for block in response.content if block.type == "text")

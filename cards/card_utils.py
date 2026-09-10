from ..llm_calls.llm_constants import MAX_TOKENS, CARD_MODEL
from ..llm_calls.client import make_client

def card_llm_combination(llm_instructions, formatted_item):
    client = make_client()
    response = client.messages.create(
        model=CARD_MODEL,
        max_tokens=MAX_TOKENS,
        system=llm_instructions,
        messages=[{"role": "user", "content": formatted_item}],
    )


    
import json
import time

from llm_calls.client import make_client
from llm_calls.instructions import card_rejection
from llm_calls.llm_constants import CARD_EFFORT, CARD_MODEL, MAX_TOKENS


def llm_call_card_formation(llm_instructions, card_content, rejected=()):
    """One card from the model. Returns the reply text and what the call cost in tokens and time.

    card_content is the dict instructions_cap describes to the model: "item",
    "recent_generations", "student" and "sentence_plan". It is serialized here rather than
    retyped into a sentence, and ensure_ascii keeps the Greek readable in the prompt. The
    instructions are marked cacheable, since every card sends the same ones.

    rejected holds earlier attempts at this same card as (reply, findings) pairs. They are
    replayed as the conversation so far, so the model sees what it wrote and why it was sent
    back, rather than starting cold and making the same card again.

    The student block goes first, as its own cached block: it is the same on every card for a
    student and runs to several thousand tokens, so after the first card it is read at the cache
    rate. The item, its history and its plan follow."""
    student = {"student": card_content.get("student")}
    rest = {key: value for key, value in card_content.items() if key != "student"}
    messages = [{"role": "user", "content": [
        {"type": "text", "text": json.dumps(student, indent=2, ensure_ascii=False),
         "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": json.dumps(rest, indent=2, ensure_ascii=False)},
    ]}]
    for reply, findings in rejected:
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": card_rejection.format(
            findings="\n".join(f"- {finding}" for finding in findings))})
    started = time.time()
    response = make_client().messages.create(
        model=CARD_MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "adaptive"},
        output_config={"effort": CARD_EFFORT},
        system=[{"type": "text", "text": llm_instructions, "cache_control": {"type": "ephemeral"}}],
        messages=messages,
    )
    usage = {
        "model": CARD_MODEL, "effort": CARD_EFFORT, "seconds": round(time.time() - started, 1),
        "input": response.usage.input_tokens,
        "cache_write": getattr(response.usage, "cache_creation_input_tokens", 0) or 0,
        "cache_read": getattr(response.usage, "cache_read_input_tokens", 0) or 0,
        "output": response.usage.output_tokens, "stop_reason": response.stop_reason,
    }
    if response.stop_reason == "refusal":
        raise RuntimeError(f"the model declined the card: {getattr(response, 'stop_details', None)}")
    if response.stop_reason == "max_tokens":
        raise RuntimeError(f"the reply ran out of room at {MAX_TOKENS} tokens (thinking counts against it)")
    return next(block.text for block in response.content if block.type == "text"), usage

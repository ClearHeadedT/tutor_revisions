"""Two one-off experiments, each changing exactly one thing against the measured
baseline in testing/output/.

    python -m testing.experiments model     # 1 call:  same syntax item, Opus 5 at low effort
    python -m testing.experiments batch     # 2 calls: one vocabulary card alone, then five
                                            #          in a single prompt, for comparison
    python -m testing.experiments           # all three calls

The batch test generates its own control rather than borrowing a card from the main run,
so both of its numbers come from the same model, effort and conditions. Results land in
testing/output_experiments/, and every raw reply is written there whether it parses or not.
"""
import json
import pathlib
import re
import sys
import time

from llm_calls.client import make_client
from tasks.new_card_creation.utils import card_instructions_loader
from testing.harness import PRICING, extract_json, item_content, item_for
from testing.items import CARD_TYPES, TEST_STUDENT

OUT = pathlib.Path(__file__).parent / "output_experiments"
SYNTAX_ITEM = "genitive/adjectival/descriptive-genitive"
VOCAB_BATCH = ["βαπτίζω", "κράζω", "διώκω", "θεραπεύω", "θύρα"]

BATCH_ADDENDUM = """

THIS REQUEST CARRIES SEVERAL ITEMS, and this section overrides the OUTPUT FORMAT above.
Where the description above says "item", this request instead carries "items": a list of
them. Everything else applies to each item separately. Build one card per item, giving each the
same reflection you would give a card written on its own -- they are independent cards
that happen to share a request, not a set, and they should not converge on a shared shape
or a shared kind of scene.
Return ONLY a JSON ARRAY wrapped in triple backticks, holding one card object per item in
the order the items were given. Each object carries exactly the keys described above.
"""


def run_call(system, content, model, effort, max_tokens=16000, stream=False):
    """stream is for the batch call: a large max_tokens on a non-streaming request can
    outrun the SDK's HTTP timeout, and streaming costs the same tokens either way."""
    started = time.time()
    params = dict(
        model=model,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        output_config={"effort": effort},
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": json.dumps(content, indent=2, ensure_ascii=False)}],
    )
    client = make_client()
    if stream:
        with client.messages.stream(**params) as streamed:
            response = streamed.get_final_message()
    else:
        response = client.messages.create(**params)
    usage = response.usage
    spend = {
        "model": model, "effort": effort, "seconds": round(time.time() - started, 1),
        "input": usage.input_tokens,
        "cache_write": getattr(usage, "cache_creation_input_tokens", 0),
        "cache_read": getattr(usage, "cache_read_input_tokens", 0),
        "output": usage.output_tokens,
        "stop_reason": response.stop_reason,
        "blocks": [b.type for b in response.content],
    }
    details = getattr(response, "stop_details", None)
    if details is not None:
        spend["stop_details"] = {"type": getattr(details, "type", None),
                                 "category": getattr(details, "category", None),
                                 "explanation": getattr(details, "explanation", None)}
    if response.stop_reason != "end_turn":
        print(f"  WARNING stop_reason={response.stop_reason} "
              f"details={spend.get('stop_details')} -- the reply may be cut short")
    text = next((b.text for b in response.content if b.type == "text"), None)
    if text is None:
        print(f"  WARNING no text block. blocks={spend['blocks']} output={usage.output_tokens}")
    return text, spend


def extract_array(reply):
    """The batch reply is an array rather than an object, fenced or not, and may carry
    a sentence of prose around it."""
    fenced = re.search(r"```(?:json)?\s*(\[.*\])\s*```", reply, re.DOTALL)
    if fenced:
        return json.loads(fenced.group(1))
    start, end = reply.find("["), reply.rfind("]")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON array in reply: {reply[:200]!r}")
    return json.loads(reply[start:end + 1])


def save(name, reply, spend, parsed=None):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(
        json.dumps({"usage": spend, "cost": cost_of_model(spend), "parsed": parsed, "reply": reply},
                   ensure_ascii=False, indent=2), encoding="utf-8")


def cost_of_model(spend):
    """Opus 5 is 5/25 per MTok against Sonnet's 2/10, so the rate depends on the model."""
    rates = ({"input": 5.0, "cache_write": 6.25, "cache_read": 0.50, "output": 25.0}
             if "opus" in spend["model"] else PRICING)
    return sum(spend.get(f, 0) * r for f, r in rates.items()) / 1_000_000


def model_test():
    """Same item, same prompt, same payload as the baseline card -- only the model and
    effort differ, so the comparison is clean."""
    system = card_instructions_loader(CARD_TYPES["syntax"])
    content = item_content("syntax", SYNTAX_ITEM)
    reply, spend = run_call(system, content, "claude-opus-5", "low")
    parsed = extract_json(reply) if reply else None
    save("model_opus5_low", reply, spend, parsed)
    print(f"opus-5 / low : out={spend['output']} in={spend['input']} "
          f"cache_write={spend['cache_write']} {spend['seconds']}s  ${cost_of_model(spend):.4f}")
    return parsed


def batch_test(model="claude-sonnet-5", effort="medium", tag="sonnet"):
    """Five vocabulary items in one request against one item in its own request, model
    and effort held constant across both. The single card is generated here rather than
    taken from the main run so both numbers come from the same conditions."""
    single_system = card_instructions_loader(CARD_TYPES["vocabulary"])
    single_reply, single_spend = run_call(
        single_system, item_content("vocabulary", VOCAB_BATCH[0]), model, effort)
    single = extract_json(single_reply) if single_reply else None
    save(f"batch_{tag}_control_single", single_reply, single_spend, single)
    single_cost = cost_of_model(single_spend)
    print(f"CONTROL  1 item, 1 call  : out={single_spend['output']:6} in={single_spend['input']:5} "
          f"cache_write={single_spend['cache_write']:5} {single_spend['seconds']:5}s  ${single_cost:.4f}")

    system = single_system + BATCH_ADDENDUM
    content = {"items": [item_for("vocabulary", key) for key in VOCAB_BATCH],
               "recent_generations": [], "student": TEST_STUDENT}
    reply, spend = run_call(system, content, model, effort,
                            max_tokens=32000, stream=True)
    parsed = None
    if reply:
        try:
            parsed = extract_array(reply)
        except Exception as error:
            print("  parse failed:", error, "-- raw reply is saved either way")
    save(f"batch_{tag}_vocab_5", reply, spend, parsed)
    cost = cost_of_model(spend)
    per = cost / len(VOCAB_BATCH)
    print(f"BATCH    5 items, 1 call : out={spend['output']:6} in={spend['input']:5} "
          f"cache_write={spend['cache_write']:5} {spend['seconds']:5}s  ${cost:.4f}  "
          f"(${per:.4f} per card)")
    print(f"  cards returned: {len(parsed) if isinstance(parsed, list) else 'PARSE FAILED'}")
    if single_cost:
        print(f"  per-card cost batched vs single: {per / single_cost:.0%}")
    return parsed


if __name__ == "__main__":
    which = sys.argv[1:] or ["model", "batch"]
    if "model" in which:
        model_test()
    if "batch" in which:
        batch_test()
    if "batch-opus" in which:
        batch_test("claude-opus-5", "low", "opus")

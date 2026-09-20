"""Generation and audit passes over the fixed sample in items.py.

Kept apart from the project: nothing here writes to a student's progress, card history,
or the shared senses cache. It reads the scaffoldings and the instructions, calls the
API, and writes everything it produces under testing/output/.

The two passes are separate on purpose. One pass generates every card of a category in
a row, which keeps the same system prompt in front of the cache for the whole run;
the audit pass then does the same with its own, much shorter, prompt.
"""
import json
import pathlib
import re

from llm_calls.client import make_client
from llm_calls.instructions import instructions_card_audit
from greek_text import normalize_greek
from tasks.new_card_creation.utils import (
    card_instructions_loader,
    unpack_grammatical_item,
    unpack_syntactic_item,
)
from testing.items import (
    GRAMMAR_ITEMS, SYNTAX_ITEMS, VOCABULARY_ITEMS, CARD_TYPES,
    SYNTAX_LEXEMES, TEST_STUDENT,
)

GENERATION_MODEL = "claude-sonnet-5"
AUDIT_MODEL = "claude-sonnet-5"

# Sonnet 5 thinks adaptively whenever thinking is left unset, and effort defaults to
# "high". Thinking is billed as output and counts against max_tokens, so an unset
# request can spend its whole ceiling reasoning and return no text at all. Constraint 8
# already asks the model to write its reflection into "reasoning", so deep invisible
# thinking on top is a second reasoning pass nobody reads.
EFFORT = "medium"
MAX_TOKENS = 16000

# Dollars per million tokens, by model. Cache writes are 1.25x the input rate, reads 0.1x.
PRICING = {"input": 2.00, "cache_write": 2.50, "cache_read": 0.20, "output": 10.00}
OPUS_PRICING = {"input": 5.00, "cache_write": 6.25, "cache_read": 0.50, "output": 25.00}

TESTING = pathlib.Path(__file__).parent
OUTPUT = TESTING / "output"
SENSES = TESTING / "data" / "vocabulary_senses.json"


def call(system, content, model, effort=None):
    """One request, with the system prompt marked cacheable and thinking bounded.
    Returns the raw reply text and the usage, and says what went wrong in terms of the
    response rather than crashing on an assumption about its shape."""
    response = make_client().messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        thinking={"type": "adaptive"},
        output_config={"effort": effort or EFFORT},
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": json.dumps(content, indent=2, ensure_ascii=False)
                   if not isinstance(content, str) else content}],
    )
    usage = response.usage
    spend = {
        "model": model,
        "input": usage.input_tokens,
        "cache_write": getattr(usage, "cache_creation_input_tokens", 0),
        "cache_read": getattr(usage, "cache_read_input_tokens", 0),
        "output": usage.output_tokens,
        "stop_reason": response.stop_reason,
        "blocks": [block.type for block in response.content],
    }
    text = next((block.text for block in response.content if block.type == "text"), None)
    if text is None:
        raise RuntimeError(
            f"no text in the reply. stop_reason={response.stop_reason}, "
            f"blocks={spend['blocks']}, output_tokens={usage.output_tokens}. "
            f"If stop_reason is max_tokens, raise MAX_TOKENS ({MAX_TOKENS}) or lower "
            f"effort (currently {effort or EFFORT!r})."
        )
    return text, spend


def extract_json(reply):
    """The model is told to return a fenced JSON object, and mostly does. This also
    survives a fence that is missing, mislabelled, or wrapped in a sentence of prose,
    because a reply that cost money should not be thrown away over its packaging."""
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", reply, re.DOTALL)
    if fenced:
        return json.loads(fenced.group(1))
    start, end = reply.find("{"), reply.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON object in reply: {reply[:200]!r}")
    return json.loads(reply[start:end + 1])


def item_for(category, key):
    """The source data for one item, as the model sees it."""
    if category == "grammar":
        return unpack_grammatical_item(key)
    if category == "syntax":
        unpacked = unpack_syntactic_item(key)
        return {"item": readable(unpacked["item"]),
                "ancestors": [readable(node) for node in unpacked["ancestors"]],
                "sibling_usages": {k: readable(v) for k, v in unpacked["sibling_usages"].items()},
                "lexical_options": SYNTAX_LEXEMES.get(key, [])}
    entry = json.loads(SENSES.read_text(encoding="utf-8"))[key]
    return {**entry["tf_lexical_info"],
            "lexical_entry": entry["lexical_entry"],
            "summary": (entry["ln_sense_info"] or {}).get("summary")}


def readable(node):
    """A usage as the card needs it. The GGBB page range and the core flag are for
    curriculum sequencing, and across fourteen siblings they are most of the block."""
    return {field: value for field, value in node.items() if field not in ("core", "source")}


def item_content(category, key):
    """What the generator is given, in the shape instructions_cap describes."""
    return {"item": item_for(category, key),
            "recent_generations": [],
            "student": TEST_STUDENT}


def keys_for(category):
    if category == "grammar":
        return GRAMMAR_ITEMS
    if category == "syntax":
        return SYNTAX_ITEMS
    return [normalize_greek(form) for form, _ in VOCABULARY_ITEMS]


def generate(category, limit=None, model=None, effort=None, out=None):
    """First pass. Every item of one category in a row, so the card-type system prompt
    stays in front of the cache for the whole category. limit stops after that many
    new cards, for running a couple at a time rather than committing to the batch.
    model, effort and out are for comparison runs; they default to the baseline."""
    model, effort, out = model or GENERATION_MODEL, effort or EFFORT, out or OUTPUT
    system = card_instructions_loader(CARD_TYPES[category])
    done = read(category, "generated", out)
    usages = []
    for key in keys_for(category):
        if key in done:
            continue
        if limit is not None and len(usages) >= limit:
            break
        reply, usage = call(system, item_content(category, key), model, effort)
        usages.append(usage)
        keep_raw(category, "generated", key, reply, usage, out)
        done[key] = extract_json(reply)
        write(category, "generated", done, out)
        print(f"  generated  {key[:52]:52} out={usage['output']:5} cache_read={usage['cache_read']}")
    return usages


def audit(category, limit=None, model=None, effort=None, out=None):
    """Second pass, over cards the first pass already produced. The auditor is never
    told which model wrote the card."""
    model, effort, out = model or AUDIT_MODEL, effort or EFFORT, out or OUTPUT
    cards = read(category, "generated", out)
    done = read(category, "audited", out)
    usages = []
    for key, card in cards.items():
        if key in done:
            continue
        if limit is not None and len(usages) >= limit:
            break
        content = {"card": card, "item": item_for(category, key), "student": TEST_STUDENT}
        reply, usage = call(instructions_card_audit, content, model, effort)
        usages.append(usage)
        keep_raw(category, "audited", key, reply, usage, out)
        done[key] = extract_json(reply)
        write(category, "audited", done, out)
        print(f"  audited    {key[:44]:44} {done[key].get('verdict', '?'):8} out={usage['output']:5} cache_read={usage['cache_read']}")
    return usages


def keep_raw(category, stage, key, reply, usage, out=None):
    """Every paid reply is written to disk before anything tries to parse it, so a
    parse failure costs a retry of the parser and not of the call."""
    path = (out or OUTPUT) / category / f"{stage}_raw.json"
    raw = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    raw[key] = {"reply": reply, "usage": usage}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")


def read(category, stage, out=None):
    path = (out or OUTPUT) / category / f"{stage}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def write(category, stage, data, out=None):
    path = (out or OUTPUT) / category / f"{stage}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def cost_of(usage):
    """What one call cost, from the usage the API reported for it. Opus is 5/25 per
    MTok against Sonnet's 2/10, so the rate follows the model that produced it."""
    rates = OPUS_PRICING if "opus" in usage.get("model", "") else PRICING
    return sum(usage.get(field, 0) * rate for field, rate in rates.items()) / 1_000_000


def report(label, usages):
    if not usages:
        print(f"{label}: nothing to do")
        return
    totals = {field: sum(u[field] for u in usages) for field in PRICING}
    print(f"{label}: {len(usages)} calls | in={totals['input']} "
          f"cache_write={totals['cache_write']} cache_read={totals['cache_read']} "
          f"out={totals['output']} | ${sum(cost_of(u) for u in usages):.3f}")


def spend(out=None):
    """Every call already paid for, read back off disk. The raw files carry the usage
    the API reported, so this is what was actually billed rather than an estimate."""
    rows = []
    for category in ("grammar", "vocabulary", "syntax"):
        for stage in ("generated", "audited"):
            path = (out or OUTPUT) / category / f"{stage}_raw.json"
            if not path.exists():
                continue
            for key, record in json.loads(path.read_text(encoding="utf-8")).items():
                usage = record["usage"]
                rows.append({"category": category, "stage": stage, "key": key,
                             "cost": cost_of(usage), **usage})
    return rows


def spend_report():
    rows = spend()
    if not rows:
        print("no calls recorded yet")
        return rows
    print(f"{'category':11} {'stage':10} {'in':>7} {'c_wr':>7} {'c_rd':>7} {'out':>7} {'stop':>12} {'cost':>8}  item")
    for row in rows:
        print(f"{row['category']:11} {row['stage']:10} {row['input']:>7} {row['cache_write']:>7} "
              f"{row['cache_read']:>7} {row['output']:>7} {str(row.get('stop_reason')):>12} "
              f"${row['cost']:>7.4f}  {row['key'][:44]}")
    total = sum(row["cost"] for row in rows)
    out = sum(row["output"] for row in rows)
    print(f"\n{len(rows)} calls | {out} output tokens | ${total:.3f} total | ${total/len(rows):.4f} per call")
    return rows

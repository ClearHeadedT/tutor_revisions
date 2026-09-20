"""Five cards per category, generated in one batched call each, audited individually.

    python -m testing.batch_run              # all three categories
    python -m testing.batch_run grammar      # one category
    python -m testing.batch_run generate     # generation pass only
    python -m testing.batch_run audit        # audit pass only, over what exists
    python -m testing.batch_run report       # free, rebuild the readable report

Generation is Opus 5 at low effort, five items in a single streamed call per category.
The audit is Sonnet 5 at medium, one card per call -- batching the auditor would split
its attention the same way batching generation does, and the audit is the instrument
the card quality is being judged with.

Output lands in testing/output_batch/ in the same shape the main harness writes, so
the audit pass and the report builder are reused rather than reimplemented.
"""
import json
import sys

from tasks.new_card_creation.utils import card_instructions_loader
from testing.experiments import BATCH_ADDENDUM, extract_array, run_call
from testing.harness import (
    OUTPUT, audit, cost_of, item_for, keep_raw, keys_for, read, write,
)
from testing.items import CARD_TYPES, TEST_STUDENT

OUT = OUTPUT.parent / "output_batch"
GENERATION = {"model": "claude-opus-5", "effort": "low"}
AUDITOR = {"model": "claude-sonnet-5", "effort": "medium"}
CATEGORIES = ["grammar", "vocabulary", "syntax"]
PER_BATCH = 5


def generate_batch(category):
    """One call producing five cards. Already-generated categories are skipped whole,
    since the batch is indivisible -- a partial batch would have to be re-paid for."""
    done = read(category, "generated", OUT)
    if done:
        print(f"  {category}: already generated ({len(done)} cards)")
        return None
    keys = keys_for(category)[:PER_BATCH]
    system = card_instructions_loader(CARD_TYPES[category]) + BATCH_ADDENDUM
    content = {"items": [item_for(category, key) for key in keys],
               "recent_generations": [], "student": TEST_STUDENT}
    reply, usage = run_call(system, content, GENERATION["model"], GENERATION["effort"],
                            max_tokens=32000, stream=True)
    # One call paid for all five, so only the first record carries the charge; the rest
    # hold the same reply for reference and are marked so cost is not counted five times.
    for position, key in enumerate(keys):
        keep_raw(category, "generated", key, reply, {**usage, "billed": position == 0}, OUT)
    if reply is None:
        print(f"  {category}: no text returned -- raw kept, nothing parsed")
        return usage
    cards = extract_array(reply)
    if len(cards) != len(keys):
        print(f"  {category}: WARNING asked for {len(keys)} cards, got {len(cards)}")
    write(category, "generated", dict(zip(keys, cards)), OUT)
    print(f"  {category}: {len(cards)} cards | out={usage['output']} "
          f"cache_write={usage['cache_write']} {usage['seconds']}s | ${cost_of(usage):.4f}")
    return usage


def run(categories, passes):
    if "generate" in passes:
        print(f"GENERATION -- {GENERATION['model']} effort={GENERATION['effort']}, "
              f"{PER_BATCH} per call")
        for category in categories:
            generate_batch(category)
    if "audit" in passes:
        print(f"\nAUDIT -- {AUDITOR['model']} effort={AUDITOR['effort']}, one card per call")
        for category in categories:
            usages = audit(category, None, AUDITOR["model"], AUDITOR["effort"], OUT)
            if usages:
                print(f"  {category}: {len(usages)} audited | "
                      f"${sum(cost_of(u) for u in usages):.4f}")
    report()


def report():
    """Cards with their verdicts, and what the run cost, read back off disk."""
    total, cards_seen = 0.0, 0
    lines = ["# Batched run -- Opus 5 low, 5 per call, audited individually by Sonnet 5", ""]
    for category in CATEGORIES:
        cards, audits = read(category, "generated", OUT), read(category, "audited", OUT)
        if not cards:
            continue
        lines += [f"## {category}", ""]
        for key, card in cards.items():
            verdict = audits.get(key) or {}
            cards_seen += 1
            lines += [f"### `{key}`", "",
                      f"> {card.get('sentence', '')}", "",
                      f"*{card.get('translation', '')}* — target `{card.get('target_form', '')}`", "",
                      f"**verdict:** {verdict.get('verdict', 'not audited')}"
                      + (f" — {verdict['summary']}" if verdict.get("summary") else ""), ""]
            blind = verdict.get("blind_reading") or {}
            if blind.get("recalls_passage"):
                lines += [f"**blind reading:** {blind.get('passage')} — "
                          f"{blind.get('what_triggered_it', '')}", ""]
            findings = [f"constraint {c['n']}: {c.get('finding')}"
                        for c in verdict.get("constraints", []) if c.get("verdict") != "holds"]
            findings += [f"echo/{c['criterion']}: {c.get('finding')}"
                         for c in verdict.get("echo", []) if c.get("verdict") != "clean"]
            reasoning = verdict.get("reasoning_audit") or {}
            if reasoning.get("sound") is False:
                findings.append(f"reasoning: {reasoning.get('finding')}")
            lines += ([f"- {f}" for f in findings] + [""]) if findings else []
            lines += ["<details><summary>reasoning</summary>", "",
                      card.get("reasoning", ""), "", "</details>", ""]
    for category in CATEGORIES:
        for stage in ("generated", "audited"):
            path = OUT / category / f"{stage}_raw.json"
            if not path.exists():
                continue
            for record in json.loads(path.read_text(encoding="utf-8")).values():
                if record["usage"].get("billed", True):
                    total += cost_of(record["usage"])
    lines.insert(1, f"\n**{cards_seen} cards, ${total:.3f} total, ${total / max(cards_seen, 1):.4f} per card.**\n")
    path = OUT / "report.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n{cards_seen} cards | ${total:.3f} total | ${total / max(cards_seen, 1):.4f} per card")
    print(f"report written to {path}")


if __name__ == "__main__":
    args = sys.argv[1:]
    chosen = [a for a in args if a in CATEGORIES] or CATEGORIES
    passes = [a for a in args if a in ("generate", "audit")] or ["generate", "audit"]
    if "report" in args:
        report()
    else:
        run(chosen, passes)

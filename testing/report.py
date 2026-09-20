"""Turns the two passes' JSON into one document meant to be read.

The JSON under testing/output/ stays as it is -- it is the resumable state and the
thing to run analysis over. This writes the human view beside it: every card with its
sentence, its reasoning, and whatever the audit found, with the passing constraints
collapsed to a count so the findings are not buried under nineteen lines of "holds".
"""
import json
import pathlib

from testing.harness import OUTPUT, read, spend
from testing.items import CARD_TYPES

REPORT = OUTPUT / "report.md"
CATEGORIES = ["grammar", "vocabulary", "syntax"]


def verdict_of(audit):
    return audit.get("verdict", "—") if audit else "not audited"


def findings(audit):
    """Only what did not pass. A clean card should print nothing here."""
    if not audit:
        return []
    out = []
    for entry in audit.get("constraints", []):
        if entry.get("verdict") != "holds":
            out.append(f"**constraint {entry.get('n')}** — {entry.get('finding', '')}")
    for entry in audit.get("echo", []):
        if entry.get("verdict") != "clean":
            passage = f" ({entry['passage']})" if entry.get("passage") else ""
            out.append(f"**echo / {entry.get('criterion')}**{passage} — {entry.get('finding', '')}")
    reasoning = audit.get("reasoning_audit") or {}
    if reasoning.get("sound") is False:
        out.append(f"**reasoning** — {reasoning.get('finding', '')}")
    return out


def card_section(key, card, audit):
    lines = [f"### `{key}`", ""]
    if card.get("sentence"):
        lines += [f"> {card['sentence']}", "", f"*{card.get('translation', '')}*", ""]
    if card.get("target_form"):
        lines.append(f"**target:** {card['target_form']}  ")
    lines.append(f"**verdict:** {verdict_of(audit)}")
    if audit and audit.get("summary"):
        lines.append(f"  — {audit['summary']}")
    lines.append("")
    blind = (audit or {}).get("blind_reading") or {}
    if blind.get("recalls_passage"):
        lines += [f"**blind reading recalled {blind.get('passage')}** — "
                  f"{blind.get('what_triggered_it', '')}", ""]
    found = findings(audit)
    if found:
        lines += ["**findings**", ""] + [f"- {f}" for f in found] + [""]
    elif audit:
        held = sum(1 for e in audit.get("constraints", []) if e.get("verdict") == "holds")
        clean = sum(1 for e in audit.get("echo", []) if e.get("verdict") == "clean")
        lines += [f"*{held} constraints hold, {clean} echo criteria clean, no findings.*", ""]
    if card.get("reasoning"):
        lines += ["<details><summary>reasoning</summary>", "", card["reasoning"], "", "</details>", ""]
    return lines


def spend_table():
    """What the run has cost so far, from the usage the API reported per call."""
    rows = spend()
    if not rows:
        return []
    lines = ["## Spend", "", "| category | stage | calls | output tokens | cost |", "|---|---|---|---|---|"]
    groups = {}
    for row in rows:
        groups.setdefault((row["category"], row["stage"]), []).append(row)
    for (category, stage), group in sorted(groups.items()):
        out = sum(r["output"] for r in group)
        lines.append(f"| {category} | {stage} | {len(group)} | {out:,} | ${sum(r['cost'] for r in group):.3f} |")
    total = sum(row["cost"] for row in rows)
    lines += [f"| **all** | | **{len(rows)}** | **{sum(r['output'] for r in rows):,}** | **${total:.3f}** |",
              "", f"${total / len(rows):.4f} per call.", ""]
    truncated = [r for r in rows if r.get("stop_reason") == "max_tokens"]
    if truncated:
        lines += [f"**{len(truncated)} call(s) hit max_tokens** and may be truncated: "
                  + ", ".join(f"`{r['key'][:40]}`" for r in truncated), ""]
    return lines


def build():
    lines = ["# Card test run", ""] + spend_table()
    for category in CATEGORIES:
        cards, audits = read(category, "generated"), read(category, "audited")
        if not cards:
            continue
        lines += [f"## {category}", "", f"Card type: `{CARD_TYPES[category]}` · "
                  f"{len(cards)} generated, {len(audits)} audited", ""]
        tally = {}
        for key in cards:
            tally[verdict_of(audits.get(key))] = tally.get(verdict_of(audits.get(key)), 0) + 1
        lines += ["| verdict | count |", "|---|---|"]
        lines += [f"| {v} | {n} |" for v, n in sorted(tally.items())]
        lines.append("")
        for key, card in cards.items():
            lines += card_section(key, card, audits.get(key))
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    return REPORT

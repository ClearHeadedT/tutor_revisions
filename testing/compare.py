"""Run the same items through two model profiles and audit both blind.

    python -m testing.compare run              # both profiles, all categories, 3 items each
    python -m testing.compare run grammar      # one category
    python -m testing.compare run grammar 1    # one category, one item per profile
    python -m testing.compare report           # rebuild the comparison from what exists

Both profiles see identical prompts and identical payloads; only the model and effort
differ. The auditor is the same for both and is never told which profile wrote a card,
so its verdicts are the one quality signal that does not come from me reading Greek.

Results live under testing/output_compare/<profile>/ in the same shape as the main run,
and every pass resumes, so this can be run a category at a time.
"""
import json
import pathlib
import sys

from testing.harness import OUTPUT, audit, cost_of, generate, read, spend

PROFILES = {
    "sonnet_medium": {"model": "claude-sonnet-5", "effort": "medium"},
    "opus_low": {"model": "claude-opus-5", "effort": "low"},
}
AUDITOR = {"model": "claude-sonnet-5", "effort": "medium"}
CATEGORIES = ["grammar", "vocabulary", "syntax"]
DEFAULT_ITEMS = 3

ROOT = OUTPUT.parent / "output_compare"


def run(categories, per_category):
    for name, profile in PROFILES.items():
        out = ROOT / name
        print(f"\n=== {name}  ({profile['model']}, effort={profile['effort']})")
        for category in categories:
            usages = generate(category, per_category, profile["model"], profile["effort"], out)
            if usages:
                print(f"  {category} generated {len(usages)} | "
                      f"${sum(cost_of(u) for u in usages):.3f}")
        for category in categories:
            usages = audit(category, per_category, AUDITOR["model"], AUDITOR["effort"], out)
            if usages:
                print(f"  {category} audited {len(usages)} | "
                      f"${sum(cost_of(u) for u in usages):.3f}")
    print()
    report()


def rows():
    """One row per card, both profiles side by side where they share an item."""
    collected = {}
    for name in PROFILES:
        out = ROOT / name
        for category in CATEGORIES:
            cards, audits = read(category, "generated", out), read(category, "audited", out)
            raws = {}
            path = out / category / "generated_raw.json"
            if path.exists():
                raws = json.loads(path.read_text(encoding="utf-8"))
            for key, card in cards.items():
                entry = collected.setdefault((category, key), {})
                entry[name] = {
                    "card": card,
                    "audit": audits.get(key),
                    "usage": raws.get(key, {}).get("usage", {}),
                }
    return collected


def report():
    collected = rows()
    if not collected:
        print("nothing generated yet")
        return
    lines = ["# Model comparison", "",
             "Same items, same prompts, same payloads. Only model and effort differ.",
             "The auditor is claude-sonnet-5 at medium effort for both, and is not told",
             "which profile wrote the card it is judging.", ""]

    lines += ["## Totals", "", "| profile | cards | output tokens | cost | per card | verdicts |",
              "|---|---|---|---|---|---|"]
    for name in PROFILES:
        entries = [e[name] for e in collected.values() if name in e]
        if not entries:
            continue
        out_tokens = sum(e["usage"].get("output", 0) for e in entries)
        cost = sum(cost_of(e["usage"]) for e in entries if e["usage"])
        verdicts = {}
        for e in entries:
            v = (e["audit"] or {}).get("verdict", "not audited")
            verdicts[v] = verdicts.get(v, 0) + 1
        tally = ", ".join(f"{n} {v}" for v, n in sorted(verdicts.items()))
        lines.append(f"| {name} | {len(entries)} | {out_tokens:,} | ${cost:.3f} | "
                     f"${cost / len(entries):.4f} | {tally} |")
    lines.append("")

    for (category, key), entry in sorted(collected.items()):
        lines += [f"## `{key}`", f"*{category}*", ""]
        for name in PROFILES:
            if name not in entry:
                continue
            card, verdict = entry[name]["card"], entry[name]["audit"] or {}
            usage = entry[name]["usage"]
            lines += [f"**{name}** — {usage.get('output', '?')} output tokens, "
                      f"verdict **{verdict.get('verdict', 'not audited')}**", "",
                      f"> {card.get('sentence', '')}", "",
                      f"*{card.get('translation', '')}* — target `{card.get('target_form', '')}`", ""]
            if verdict.get("summary"):
                lines += [f"Auditor: {verdict['summary']}", ""]
            findings = [f"constraint {c['n']}: {c.get('finding')}"
                        for c in verdict.get("constraints", []) if c.get("verdict") != "holds"]
            findings += [f"echo/{c['criterion']}: {c.get('finding')}"
                         for c in verdict.get("echo", []) if c.get("verdict") != "clean"]
            reasoning = verdict.get("reasoning_audit") or {}
            if reasoning.get("sound") is False:
                findings.append(f"reasoning: {reasoning.get('finding')}")
            if findings:
                lines += [f"- {f}" for f in findings] + [""]
            lines += ["<details><summary>reasoning</summary>", "",
                      card.get("reasoning", ""), "", "</details>", ""]

    path = ROOT / "comparison.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"comparison written to {path}")
    for name in PROFILES:
        entries = [e[name] for e in collected.values() if name in e]
        if entries:
            cost = sum(cost_of(e["usage"]) for e in entries if e["usage"])
            print(f"  {name:14} {len(entries)} cards  ${cost:.3f}")
    return path


if __name__ == "__main__":
    args = sys.argv[1:]
    chosen = [a for a in args if a in CATEGORIES] or CATEGORIES
    count = next((int(a) for a in args if a.isdigit()), DEFAULT_ITEMS)
    if "report" in args:
        report()
    else:
        run(chosen, count)

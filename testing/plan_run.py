"""The fixed sample again, each card written to a sentence plan and checked for echo before it is kept.

    python -m testing.plan_run preview              # free: the exact prompts, written to preview.md
    python -m testing.plan_run                      # generate + audit all three categories
    python -m testing.plan_run vocabulary generate  # one category, one pass
    python -m testing.plan_run report               # free: rebuild report.md, with the comparison

Generation matches batch_run's model and effort, one card per call, since each card carries its
own plan. A card the echo check flags is sent back with the finding, up to CHECK_RETRIES times;
every attempt's reply is kept. The audit is the main harness's, unchanged except that it is now
handed the measured overlap. testing/output_batch/ is the comparison: the same items, the same
auditor, written before plans existed. It was generated five to a call, which this is not.

The student behind the plans has met every grammar group and every construction the traversal
can offer, plus the core syntax items, so the sample shows the full range of shapes. The student
block the model sees is still TEST_STUDENT, with no vocabulary list, so the vocabulary check is
not run here.
"""
import json
import random
import sys

from data.student_data.student import Student
from data.student_data.student_data_helper_functions import load_grammar_scaffolding, load_syntax_scaffolding
from tasks.card_randomization.card_randomize_utils import build_sentence_plan
from tasks.new_card_creation.new_card import CHECK_RETRIES
from tasks.new_card_creation.utils import card_instructions_loader
from tasks.new_card_creation.verify import check_card
from testing.harness import (
    OUTPUT, audit, call, cost_of, extract_json, item_content, keep_raw, keys_for, read, write,
)
from testing.items import CARD_TYPES

OUT = OUTPUT.parent / "output_plan"
CONTROL = OUTPUT.parent / "output_batch"
GENERATION = {"model": "claude-opus-5", "effort": "low"}
AUDITOR = {"model": "claude-sonnet-5", "effort": "medium"}
CATEGORIES = ["grammar", "vocabulary", "syntax"]


def plan_student():
    wiring = json.loads(open("data/curriculum_data/traversal_wiring.json", encoding="utf-8").read())
    syntax = {usage["syntactic_item"] for usage in wiring.values()}
    syntax |= {key for key, item in load_syntax_scaffolding()["items"].items() if item.get("core")}
    student = object.__new__(Student)
    student.student_id, student.level = "plan_run", "beyond_beginner"
    student.grammar = {key: {} for key in load_grammar_scaffolding()["items"]}
    student.syntax = {key: {} for key in sorted(syntax)}
    student.vocabulary, student.cards, student.senses = {}, {}, {}
    return student


def plan_for(student, category, key):
    """The same plan for an item on every run, so the preview shows what generation will send."""
    random.seed(f"plan_run:{category}:{key}")
    return build_sentence_plan(student, CARD_TYPES[category], category, key)


def content_for(student, category, key):
    return {**item_content(category, key), "sentence_plan": plan_for(student, category, key)}


def generate(category, limit=None):
    student = plan_student()
    system = card_instructions_loader(CARD_TYPES[category])
    done = read(category, "generated", OUT)
    checks = read(category, "checks", OUT)
    usages = []
    for key in keys_for(category):
        if key in done or (limit is not None and len(usages) >= limit):
            continue
        content = content_for(student, category, key)
        target = key if category == "vocabulary" else None
        rejected = []
        while True:
            reply, usage = call(system, content, GENERATION["model"], GENERATION["effort"], rejected)
            usages.append(usage)
            keep_raw(category, "generated", f"{key}#{len(rejected) + 1}", reply, usage, OUT)
            card = extract_json(reply)
            check = check_card(card, target=target)
            if not check["findings"] or len(rejected) == CHECK_RETRIES:
                break
            rejected.append((reply, check["findings"]))
        done[key] = card
        checks[key] = {"attempts": len(rejected) + 1, "rejections": [f for _, f in rejected],
                       "final_findings": check["findings"], "overlap": check["overlap"],
                       "sentence_plan": content["sentence_plan"]}
        write(category, "generated", done, OUT)
        write(category, "checks", checks, OUT)
        print(f"  {key[:44]:44} attempts={len(rejected) + 1} "
              f"{'FLAGGED' if check['findings'] else 'clean  '} setting={card.get('setting')}")
    return usages


def preview():
    """Every prompt generation would send, without sending it."""
    student = plan_student()
    lines = ["# Plan run preview", "", "No API calls. Each item's user message as generation would send it; "
             "the system prompt is the card type's instructions and is the same for every item of a category.", ""]
    for category in CATEGORIES:
        lines += [f"## {category} — `{CARD_TYPES[category]}`", ""]
        for key in keys_for(category):
            lines += [f"### `{key}`", "", "```json",
                      json.dumps(content_for(student, category, key), indent=2, ensure_ascii=False), "```", ""]
    system = card_instructions_loader(CARD_TYPES["vocabulary"])
    lines += ["## System prompt (vocabulary)", "", "```", system, "```", ""]
    path = OUT / "preview.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"preview written to {path}")


def echo_outcome(audit_record):
    echo = {e.get("criterion"): e.get("verdict") for e in (audit_record or {}).get("echo", [])}
    if any(v == "fails" for v in echo.values()):
        return "fails"
    if any(v == "concern" for k, v in echo.items() if k in ("wording", "structure", "scene")):
        return "concern"
    return "clean" if audit_record else "not audited"


def comparison():
    """Plan run against the batch run, per category: auditor verdicts, echo outcomes, and how
    often the blind reading recalled a passage."""
    lines = ["| category | run | cards | keep / revise / discard | echo clean / concern / fails | blind recall |",
             "|---|---|---|---|---|---|"]
    for category in CATEGORIES:
        for label, out in (("batch (no plan)", CONTROL), ("plan", OUT)):
            cards, audits = read(category, "generated", out), read(category, "audited", out)
            if not cards:
                continue
            verdicts = [audits.get(k, {}).get("verdict") for k in cards]
            echoes = [echo_outcome(audits.get(k)) for k in cards]
            recalls = sum(bool((audits.get(k, {}).get("blind_reading") or {}).get("recalls_passage")) for k in cards)
            lines.append(f"| {category} | {label} | {len(cards)} | "
                         f"{verdicts.count('keep')} / {verdicts.count('revise')} / {verdicts.count('discard')} | "
                         f"{echoes.count('clean')} / {echoes.count('concern')} / {echoes.count('fails')} | "
                         f"{recalls}/{len(cards)} |")
    return lines


def report():
    total, lines = 0.0, ["# Plan run", "", "## Against the batch run", ""] + comparison() + [""]
    for category in CATEGORIES:
        cards, audits, checks = (read(category, stage, OUT) for stage in ("generated", "audited", "checks"))
        if not cards:
            continue
        lines += [f"## {category}", ""]
        for key, card in cards.items():
            verdict, check = audits.get(key) or {}, checks.get(key) or {}
            plan = check.get("sentence_plan", {})
            setting = plan.get("setting_options", {}).get(str(card.get("setting", "")).removeprefix("adapted:"))
            lines += [f"### `{key}`", "",
                      f"*shape:* {plan.get('sentence_shape', {}).get('shape')}  ",
                      f"*also include:* {', '.join(e['name'] for e in plan.get('also_include', [])) or '—'}  ",
                      f"*setting:* {card.get('setting')} — {setting}  ",
                      f"*attempts:* {check.get('attempts')}"
                      + (f" — sent back for: {check['rejections']}" if check.get("rejections") else ""), "",
                      f"> {card.get('sentence', '')}", "",
                      f"*{card.get('translation', '')}* — target `{card.get('target_form', '')}`", "",
                      f"**verdict:** {verdict.get('verdict', 'not audited')}"
                      + (f" — {verdict['summary']}" if verdict.get("summary") else ""), ""]
            blind = verdict.get("blind_reading") or {}
            if blind.get("recalls_passage"):
                lines += [f"**blind reading:** {blind.get('passage')} — {blind.get('what_triggered_it', '')}", ""]
    for category in CATEGORIES:
        for stage in ("generated", "audited"):
            path = OUT / category / f"{stage}_raw.json"
            if path.exists():
                total += sum(cost_of(r["usage"]) for r in json.loads(path.read_text(encoding="utf-8")).values())
    lines.insert(1, f"\n**${total:.3f} spent on this run.**\n")
    path = OUT / "report.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"report written to {path} | ${total:.3f} spent")


if __name__ == "__main__":
    args = sys.argv[1:]
    chosen = [a for a in args if a in CATEGORIES] or CATEGORIES
    if "preview" in args:
        preview()
    elif "report" in args:
        report()
    else:
        passes = [a for a in args if a in ("generate", "audit")] or ["generate", "audit"]
        if "generate" in passes:
            print(f"GENERATION -- {GENERATION['model']} effort={GENERATION['effort']}, one card per call")
            for category in chosen:
                generate(category)
        if "audit" in passes:
            print(f"\nAUDIT -- {AUDITOR['model']} effort={AUDITOR['effort']}")
            for category in chosen:
                audit(category, None, AUDITOR["model"], AUDITOR["effort"], OUT)
        report()

"""Cards for the fixed sample, written the way production writes them, for reading and timing.

    python -m testing.plan_run preview           # free: the exact prompts, written to preview.md
    python -m testing.plan_run vocabulary 1      # one card; any category, any count
    python -m testing.plan_run                   # every item of every category
    python -m testing.plan_run report            # free: rebuild report.md from what exists

Each card goes through production's own loop - tasks.new_card_creation.new_card.form_checked_card
- with the model and effort in llm_calls/llm_constants.py: generated, checked against the GNT word
by word and for vocabulary, and sent back with the findings up to CHECK_RETRIES times.
Every attempt is kept with its reply, time and tokens. There is no auditor; the report sets out the
card, its plan and every check for reading.

The student is test_student (see testing/make_test_student.py). Nothing is written to its
progress or card history, and the shared senses file is not touched: vocabulary items come from
testing/data/vocabulary_senses.json.
"""
import json
import random
import sys

from data.student_data.student import Student
from tasks.card_randomization.card_randomize_utils import build_sentence_plan
from tasks.new_card_creation.new_card import form_checked_card
from tasks.new_card_creation.utils import card_instructions_loader
from testing.harness import OUTPUT, cost_of, item_for, keys_for, read, write
from testing.items import CARD_TYPES

OUT = OUTPUT.parent / "output_plan"
CATEGORIES = ["grammar", "vocabulary", "syntax"]
STUDENT_ID = "test_student"


def plan_for(student, category, key):
    """The same plan for an item on every run, so the preview shows what generation will send."""
    random.seed(f"plan_run:{category}:{key}")
    return build_sentence_plan(student, CARD_TYPES[category], category, key)


def content_for(student, category, key):
    return {"item": item_for(category, key), "recent_generations": [],
            "student": student.student_overview(), "sentence_plan": plan_for(student, category, key)}


def targets_for(category, key):
    """What the card is held to: a vocabulary card's lemma, a grammar card's parse and GNT forms, a
    syntax card's GNT pairings."""
    if category == "vocabulary":
        return key, None, None, None
    item = item_for(category, key)["item"]
    if category == "grammar":
        return None, item.get("features"), [form["form"] for form in item["gnt_forms"]], None
    return None, None, None, item.get("gnt_lexemes")


def generate(category, limit=None):
    student = Student(STUDENT_ID)
    system = card_instructions_loader(CARD_TYPES[category])
    done, checks = read(category, "generated", OUT), read(category, "checks", OUT)
    made = 0
    for key in keys_for(category):
        if key in done:
            continue
        if limit is not None and made >= limit:
            break
        content = content_for(student, category, key)
        target, target_features, target_forms, target_lexemes = targets_for(category, key)
        card = form_checked_card(system, content, student, target, target_features, target_forms,
                                 target_lexemes, keep_replies=True)
        check = card.pop("check")
        done[key] = card
        checks[key] = {**check, "sentence_plan": content["sentence_plan"]}
        write(category, "generated", done, OUT)
        write(category, "checks", checks, OUT)
        made += 1
        attempts = check["attempts"]
        print(f"  {key[:40]:40} attempts={len(attempts)} seconds={check['seconds']:6} "
              f"{'KEPT WITH FINDINGS' if check['findings'] else 'passed'} "
              f"${sum(cost_of(a) for a in attempts):.4f}")
        for number, attempt in enumerate(attempts, start=1):
            print(f"      attempt {number}: {attempt['seconds']}s out={attempt['output']} "
                  f"cache_read={attempt['cache_read']} findings={len(attempt['findings'])}")


def preview():
    """Every prompt generation would send, without sending it."""
    student = Student(STUDENT_ID)
    lines = ["# Plan run preview", "", "No API calls. Each item's user message as generation would send it; "
             "the system prompt is the card type's instructions and is the same for every item of a category.", ""]
    for category in CATEGORIES:
        lines += [f"## {category} - `{CARD_TYPES[category]}`", ""]
        for key in keys_for(category):
            content = content_for(student, category, key)
            content["student"] = "(the test student's block: level, grammar learned, syntax learned, 500 words)"
            lines += [f"### `{key}`", "", "```json", json.dumps(content, indent=2, ensure_ascii=False), "```", ""]
    lines += ["## System prompt (vocabulary)", "", "```", card_instructions_loader(CARD_TYPES["vocabulary"]), "```", ""]
    path = OUT / "preview.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"preview written to {path}")


def card_section(key, card, check):
    plan = check.get("sentence_plan", {})
    setting_id = str(card.get("setting", "")).removeprefix("adapted:")
    attempts = check.get("attempts", [])
    lines = [f"### `{key}`", "",
             f"**{card.get('sentence', '(no card)')}**", "",
             f"*{card.get('translation', '')}* - target `{card.get('target_form', '')}`", "",
             f"- shape: {plan.get('sentence_shape', {}).get('shape')}",
             f"- extra, one of: {' | '.join(o.split(' - ')[0] for o in plan.get('also_include_one_of', [])) or '-'}",
             f"- setting: {card.get('setting')} - {plan.get('setting_options', {}).get(setting_id, '')}",
             f"- attempts: {len(attempts)}, {check.get('seconds')}s, "
             f"${sum(cost_of(a) for a in attempts):.4f}",
             f"- unknown words glossed: {card.get('helps') or '-'}", ""]
    for number, attempt in enumerate(attempts, start=1):
        lines.append(f"  - attempt {number}: {attempt['seconds']}s, {attempt['output']} output tokens"
                     + (": sent back for " + " / ".join(attempt["findings"]) if attempt["findings"] and
                        number < len(attempts) else ""))
    if check.get("findings"):
        lines += ["", "**kept with findings:**", ""] + [f"- {f}" for f in check["findings"]]
    if check.get("notes"):
        lines += ["", "notes:", ""] + [f"- {n}" for n in check["notes"]]
    lines += ["", "| word | given as | GNT check |", "|---|---|---|"]
    lines += [f"| {w['form']} | {w.get('given', '-')} | {w['status']}{' - ' + w['gnt'] if w.get('gnt') else ''} |"
              for w in check.get("words", [])]
    lines.append("")
    if card.get("reasoning"):
        lines += ["<details><summary>reasoning</summary>", "", card["reasoning"], "", "</details>", ""]
    return lines


def report():
    lines, total_cost, total_seconds, cards = ["# Plan run", ""], 0.0, 0.0, 0
    for category in CATEGORIES:
        generated, checks = read(category, "generated", OUT), read(category, "checks", OUT)
        if not generated:
            continue
        lines += [f"## {category}", ""]
        for key, card in generated.items():
            check = checks.get(key, {})
            total_cost += sum(cost_of(a) for a in check.get("attempts", []))
            total_seconds += check.get("seconds") or 0
            cards += 1
            lines += card_section(key, card, check)
    lines.insert(1, f"\n**{cards} cards, ${total_cost:.3f}, {total_seconds:.0f}s of generation.**\n")
    path = OUT / "report.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"report written to {path} | {cards} cards | ${total_cost:.3f} | {total_seconds:.0f}s")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "preview" in args:
        preview()
    elif "report" in args:
        report()
    else:
        limit = next((int(a) for a in args if a.isdigit()), None)
        for category in [a for a in args if a in CATEGORIES] or CATEGORIES:
            print(f"{category} - {CARD_TYPES[category]}")
            generate(category, limit)
        report()

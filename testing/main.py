"""Run the card test sample.

    python -m testing.main            # generate every category, then audit every category
    python -m testing.main generate   # first pass only
    python -m testing.main audit      # second pass only, over what is already generated
    python -m testing.main report     # rebuild the readable report from what exists
    python -m testing.main cost       # what every call already made actually cost
    python -m testing.main generate grammar

Both passes skip items already written under testing/output/, so a run that stops part
way -- or runs out of credit -- picks up where it left off rather than paying twice.
Every run rewrites testing/output/report.md, which is the copy meant to be read.
"""
import sys

from testing.harness import generate, audit, report, spend_report
from testing.report import build

CATEGORIES = ["grammar", "vocabulary", "syntax"]


def run(passes, categories, limit=None):
    if "generate" in passes:
        print("GENERATION PASS")
        for category in categories:
            print(f" {category}")
            report(f" {category} generation", generate(category, limit))
    if "audit" in passes:
        print("\nAUDIT PASS")
        for category in categories:
            print(f" {category}")
            report(f" {category} audit", audit(category, limit))
    print(f"\nreport written to {build()}")


if __name__ == "__main__":
    args = sys.argv[1:]
    chosen_passes = [a for a in args if a in ("generate", "audit", "report", "cost")]
    chosen_limit = next((int(a) for a in args if a.isdigit()), None)
    if chosen_passes == ["cost"]:
        spend_report()
    elif chosen_passes == ["report"]:
        print(f"report written to {build()}")
    else:
        chosen_categories = [a for a in args if a in CATEGORIES] or CATEGORIES
        run(chosen_passes or ["generate", "audit"], chosen_categories, chosen_limit)

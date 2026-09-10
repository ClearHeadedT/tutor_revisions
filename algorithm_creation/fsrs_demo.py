"""Worked example. Run directly: python3 algorithm_creation/fsrs_demo.py"""

from datetime import date, timedelta

from algorithm_creation.fsrs import (
    AGAIN, HARD, GOOD, EASY,
    next_interval, retrievability, review_card,
)

RATING_NAMES = {AGAIN: "Again", HARD: "Hard", GOOD: "Good", EASY: "Easy"}


def check_invariants():
    for stability in (0.5, 2.3065, 17.0, 365.0):
        assert round(retrievability(stability, stability), 12) == 0.9
        assert next_interval(stability, desired_retention=0.9) == max(round(stability), 1)
    print("invariants hold: R(S, S) == 0.9, and interval == stability at 90% retention\n")


def show_first_review():
    today = date(2026, 9, 9)
    print("a brand new card, graded each of the four ways")
    for rating in (AGAIN, HARD, GOOD, EASY):
        card = review_card({}, rating, today)
        print(f"  {RATING_NAMES[rating]:<6} S={card['stability']:>8.4f}  "
              f"D={card['difficulty']:>6.4f}  due {card['due']}")
    print()


def show_history():
    card = {}
    review_date = date(2026, 9, 9)
    print("one card over a run of reviews")
    for rating in (GOOD, GOOD, GOOD, AGAIN, GOOD, EASY):
        elapsed = 0 if not card else (review_date - date.fromisoformat(card["last_reviewed"])).days
        recall = retrievability(elapsed, card["stability"]) if card else 1.0
        card = review_card(card, rating, review_date)
        interval = (date.fromisoformat(card["due"]) - review_date).days
        print(f"  {review_date}  {RATING_NAMES[rating]:<6} R={recall:>5.3f} -> "
              f"S={card['stability']:>8.3f}  D={card['difficulty']:>6.3f}  next in {interval:>4} days")
        review_date = date.fromisoformat(card["due"])
    print()


if __name__ == "__main__":
    check_invariants()
    show_first_review()
    show_history()

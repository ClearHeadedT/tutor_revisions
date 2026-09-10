"""FSRS-6 scheduler. Given a card's memory state and a grade, produce the new state and next due date."""

import math
from datetime import date, timedelta


DEFAULT_PARAMETERS = (0.212, 1.2931, 2.3065, 8.2956, 6.4133, 0.8334, 3.0194, 0.001,
                      1.8722, 0.1666, 0.796, 1.4835, 0.0614, 0.2629, 1.6483, 0.6014,
                      1.8729, 0.5425, 0.0912, 0.0658, 0.1542)

AGAIN, HARD, GOOD, EASY = 1, 2, 3, 4

STABILITY_MIN = 0.001
DIFFICULTY_MIN = 1.0
DIFFICULTY_MAX = 10.0


def decay(parameters=DEFAULT_PARAMETERS):
    return -parameters[20]


def factor(parameters=DEFAULT_PARAMETERS):
    return 0.9 ** (1 / decay(parameters)) - 1


def clamp_stability(stability):
    return max(stability, STABILITY_MIN)


def clamp_difficulty(difficulty):
    return min(max(difficulty, DIFFICULTY_MIN), DIFFICULTY_MAX)


def retrievability(elapsed_days, stability, parameters=DEFAULT_PARAMETERS):
    """Probability of recall right now, given days since the last review."""
    return (1 + factor(parameters) * elapsed_days / stability) ** decay(parameters)


def initial_stability(rating, parameters=DEFAULT_PARAMETERS):
    return clamp_stability(parameters[rating - 1])


def initial_difficulty(rating, parameters=DEFAULT_PARAMETERS, clamp=True):
    difficulty = parameters[4] - math.e ** (parameters[5] * (rating - 1)) + 1
    if clamp:
        return clamp_difficulty(difficulty)
    return difficulty


def next_difficulty(difficulty, rating, parameters=DEFAULT_PARAMETERS):
    delta = -(parameters[6] * (rating - 3))
    damped = difficulty + (10.0 - difficulty) * delta / 9.0
    easy_difficulty = initial_difficulty(EASY, parameters, clamp=False)
    reverted = parameters[7] * easy_difficulty + (1 - parameters[7]) * damped
    return clamp_difficulty(reverted)


def recall_stability(difficulty, stability, recall_probability, rating, parameters=DEFAULT_PARAMETERS):
    hard_penalty = parameters[15] if rating == HARD else 1
    easy_bonus = parameters[16] if rating == EASY else 1
    return stability * (
        1
        + math.e ** parameters[8]
        * (11 - difficulty)
        * stability ** -parameters[9]
        * (math.e ** ((1 - recall_probability) * parameters[10]) - 1)
        * hard_penalty
        * easy_bonus
    )


def forget_stability(difficulty, stability, recall_probability, parameters=DEFAULT_PARAMETERS):
    long_term = (
        parameters[11]
        * difficulty ** -parameters[12]
        * ((stability + 1) ** parameters[13] - 1)
        * math.e ** ((1 - recall_probability) * parameters[14])
    )
    short_term = stability / math.e ** (parameters[17] * parameters[18])
    return min(long_term, short_term)


def next_stability(difficulty, stability, recall_probability, rating, parameters=DEFAULT_PARAMETERS):
    if rating == AGAIN:
        stability = forget_stability(difficulty, stability, recall_probability, parameters)
    else:
        stability = recall_stability(difficulty, stability, recall_probability, rating, parameters)
    return clamp_stability(stability)


def short_term_stability(stability, rating, parameters=DEFAULT_PARAMETERS):
    """Used when a card is reviewed again the same day, so no time has passed."""
    increase = math.e ** (parameters[17] * (rating - 3 + parameters[18])) * stability ** -parameters[19]
    if rating != AGAIN:
        increase = max(increase, 1.0)
    return clamp_stability(stability * increase)


def next_interval(stability, desired_retention=0.9, parameters=DEFAULT_PARAMETERS, maximum_interval=36500):
    """Days until the card should next be seen. At 90% retention this equals stability."""
    interval = (stability / factor(parameters)) * (desired_retention ** (1 / decay(parameters)) - 1)
    return min(max(round(interval), 1), maximum_interval)


def review_card(card, rating, review_date, desired_retention=0.9,
                parameters=DEFAULT_PARAMETERS, maximum_interval=36500):
    """Returns a new card dict with the updated memory state. Does not modify the one passed in."""
    if "stability" not in card:
        stability = initial_stability(rating, parameters)
        difficulty = initial_difficulty(rating, parameters)
    else:
        elapsed_days = max(0, (review_date - date.fromisoformat(card["last_reviewed"])).days)
        if elapsed_days == 0:
            stability = short_term_stability(card["stability"], rating, parameters)
        else:
            recall_probability = retrievability(elapsed_days, card["stability"], parameters)
            stability = next_stability(card["difficulty"], card["stability"], recall_probability, rating, parameters)
        difficulty = next_difficulty(card["difficulty"], rating, parameters)

    interval = next_interval(stability, desired_retention, parameters, maximum_interval)

    reviewed_card = dict(card)
    reviewed_card["stability"] = stability
    reviewed_card["difficulty"] = difficulty
    reviewed_card["last_reviewed"] = review_date.isoformat()
    reviewed_card["due"] = (review_date + timedelta(days=interval)).isoformat()
    return reviewed_card

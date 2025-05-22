# components/performance_evaluator.py

import random

# Import ideal performance data
from .ideal_data import (
    bicep_curl_estimates_boys, bicep_curl_estimates_girls,
    squat_estimates_boys, squat_estimates_girls,
    pushup_estimates_boys, pushup_estimates_girls,
    plank_estimates_boys, plank_estimates_girls
)

def random_prompt():
    """Return a random prompt key like 'Prompt 3'."""
    return f"Prompt {random.randint(1, 5)}"

def evaluate_performance(workout_choice, rep_or_time, age, gender):
    """
    Returns (prompt_key, tone_key) for email generation
    based on user performance compared to ideal.
    """

    gender = gender.upper()
    if gender not in ["M", "F"]:
        raise ValueError("Gender must be 'M' or 'F'")

    is_male = gender == "M"

    # Select the ideal value based on workout, age, and gender
    try:
        if workout_choice == 1:  # Bicep Curls
            ideal = bicep_curl_estimates_boys[age] if is_male else bicep_curl_estimates_girls[age]
        elif workout_choice == 2:  # Squats
            ideal = squat_estimates_boys[age] if is_male else squat_estimates_girls[age]
        elif workout_choice == 3:  # Push-ups
            ideal = pushup_estimates_boys[age] if is_male else pushup_estimates_girls[age]
        elif workout_choice == 4:  # Plank (duration in seconds)
            ideal = plank_estimates_boys[age] if is_male else plank_estimates_girls[age]
        else:
            raise ValueError("Invalid workout choice.")
    except KeyError:
        raise ValueError(f"No ideal data found for age {age}.")

    # Decide tone based on performance
    if rep_or_time > ideal + 5:
        tone = "awesome_email"
    elif rep_or_time < ideal - 5:
        tone = "poor_email"
    else:
        tone = "good_email"

    return random_prompt(), tone

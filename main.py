# app.py — Streamlit App with Multi-Workout, Email, and Logging

import streamlit as st
import time
import pandas as pd
from components.workout_tracker import track_workout
from components.email_handler import send_custom_email
import os
from datetime import datetime

st.set_page_config(page_title="Fitness Tracker", layout="centered")
st.title("🏋️ Fitness Assessment Tracker")

# Workout selection
workout_options = {
    "Bicep Curls": 1,
    "Squats": 2,
    "Push-ups": 3,
    "Plank": 4
}

selected_workout = st.selectbox("Select a workout to perform", ["-- Select --"] + list(workout_options.keys()))
duration_minutes = st.slider("Duration (minutes)", 0.5, 5.0, 1.0, step=0.5)
user_name = st.text_input("Your Name")
user_email = st.text_input("Your Email")

start_button = st.button("Start Workout")

if start_button and selected_workout != "-- Select --" and user_name and user_email:
    st.info(f"Starting {selected_workout} for {duration_minutes} minutes...")
    workout_choice = workout_options[selected_workout]
    end_time = time.time() + duration_minutes * 60

    rep_count, plank_duration = track_workout(workout_choice, end_time)

    if workout_choice == 4:
        st.success(f"✅ You held the plank for {plank_duration:.2f} seconds.")
        result_summary = f"Plank Duration: {plank_duration:.2f} seconds"
    else:
        st.success(f"✅ You completed {rep_count} {selected_workout} reps!")
        result_summary = f"Repetitions: {rep_count}"

    # Choose email tone based on performance
    if workout_choice == 4:
        tone = "awesome_email" if plank_duration >= 30 else "poor_email"
    else:
        tone = "awesome_email" if rep_count >= 10 else "good_email"

    prompt_key = "Prompt 1"  # You can randomize or rotate if desired
    send_custom_email(user_name, user_email, tone, prompt_key)
    st.success("📩 Email summary sent!")

    # Save result to Excel
    log_file = "fitness_log.xlsx"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result_data = pd.DataFrame([[now, user_name, selected_workout, rep_count if workout_choice != 4 else plank_duration]],
                                columns=["Date", "Name", "Workout", "Performance"])

    if os.path.exists(log_file):
        old_data = pd.read_excel(log_file)
        combined = pd.concat([old_data, result_data], ignore_index=True)
    else:
        combined = result_data

    combined.to_excel(log_file, index=False)
    st.success("📊 Workout logged to Excel successfully!")

elif start_button:
    st.warning("⚠️ Please fill in all fields and select a workout.")

# app.py — Full Streamlit App with Workout Tracking, Email Feedback, and Excel Logging

import streamlit as st
import time
import pandas as pd
import os
from datetime import datetime

from components.workout_tracker import track_workout
from components.email_handler import send_custom_email
from components.performance_evaluator import evaluate_performance

st.set_page_config(page_title="Fitness Assessment App", layout="centered")
st.title("🏋️ Fitness Assessment Tracker")

# -------------------- User Input -------------------- #
user_name = st.text_input("👤 Enter your name")
user_email = st.text_input("📧 Enter your email")
user_age = st.number_input("🎂 Enter your age", min_value=5, max_value=100, step=1)
user_gender = st.radio("⚧️ Select your gender", ["M", "F"], horizontal=True)

# Workout options
workout_options = {
    "Bicep Curls": 1,
    "Squats": 2,
    "Push-ups": 3,
    "Plank": 4
}
selected_workout = st.selectbox("🏋️ Select your workout", ["-- Select --"] + list(workout_options.keys()))
duration_minutes = st.slider("⏱️ Workout duration (in minutes)", 0.5, 5.0, 1.0, step=0.5)

start_button = st.button("🚀 Start Workout")

# -------------------- Workout Execution -------------------- #
if start_button:
    if not user_name or not user_email or selected_workout == "-- Select --":
        st.warning("⚠️ Please fill all details and select a workout.")
    else:
        st.info(f"Starting {selected_workout} for {duration_minutes} minutes...")
        workout_choice = workout_options[selected_workout]
        end_time = time.time() + duration_minutes * 60

        rep_count, plank_duration = track_workout(workout_choice, end_time)

        if workout_choice == 4:
            performance = plank_duration
            st.success(f"✅ You held the plank for {plank_duration:.2f} seconds.")
        else:
            performance = rep_count
            st.success(f"✅ You completed {rep_count} {selected_workout} reps!")

        # -------------------- Evaluate & Email -------------------- #
        try:
            prompt_key, tone = evaluate_performance(workout_choice, performance, user_age, user_gender)
            ideal = evaluate_performance(workout_choice, user_age, user_gender)
            send_custom_email(user_name, user_email, tone, prompt_key, performance, ideal)
            st.success("📩 Feedback email sent successfully!")
        except Exception as e:
            st.error(f"Email failed: {e}")

        # -------------------- Log to Excel -------------------- #
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = "fitness_log.xlsx"
        new_data = pd.DataFrame([[now, user_name, user_email, user_gender, user_age, selected_workout, performance]],
                                columns=["Date", "Name", "Email", "Gender", "Age", "Workout", "Performance"])

        if os.path.exists(log_file):
            old_data = pd.read_excel(log_file)
            all_data = pd.concat([old_data, new_data], ignore_index=True)
        else:
            all_data = new_data

        all_data.to_excel(log_file, index=False)
        st.success("📊 Workout logged successfully!")

# -------------------- Sidebar Notes -------------------- #
st.sidebar.markdown("""
### Notes:
- This app works with your local webcam only.
- Please use `streamlit run app.py` to start locally.
- Webcam features do not work on Streamlit Cloud.
""")

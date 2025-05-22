import streamlit as st
from components.camera import run_camera
from components.email_handler import send_test_email
from components.workout_tracker import track_workout
import time


st.set_page_config(page_title="Fitness Assessment App", layout="centered")
st.title("Fitness Assessment App")

st.markdown("### Choose your workout:")
workout_name = st.selectbox("Select a workout", ["-- Select --", "Bicep Curls", "Squats", "Push-ups", "Plank"])
duration_min = st.slider("Workout Duration (minutes)", min_value=0, max_value=10, value=1)

start_button = st.button("Start Workout")
if start_button and workout_name != "-- Select --":
    workout_choice_map = {
        "Bicep Curls": 1,
        "Squats": 2,
        "Push-ups": 3,
        "Plank": 4
    }

    workout_choice = workout_choice_map[workout_name]
    end_time = time.time() + duration_min * 60  # in seconds

    st.info("Starting workout. Close the window or press 'e' to end early.")
    rep_count, plank_duration = track_workout(workout_choice, end_time)

    # Display Results
    if workout_choice == 4:
        st.success(f"You held the plank for {plank_duration:.2f} seconds.")
    else:
        st.success(f"You completed {rep_count} repetitions of {workout_name}.")

if st.checkbox("Start Webcam (local only)"):
    run_camera()

st.markdown("---")

if st.button("Send Test Email"):
    send_test_email("Vishal", "example@example.com")

st.sidebar.info("Note: Webcam only works in local Streamlit runs.")
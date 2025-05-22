# components/workout_tracker.py — Streamlit Compatible Version

import cv2
import numpy as np
import time
import mediapipe as mp
import streamlit as st

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180 else angle

def track_workout(workout_choice, end_time):
    cap = cv2.VideoCapture(0)
    rep_count = 0
    plank_duration = 0
    in_down_position = False
    last_command = None
    plank_start_time = None

    frame_display = st.empty()

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.warning("Camera not accessible.")
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                landmarks = results.pose_landmarks.landmark

                # Workout detection logic
                if workout_choice == 1:  # Bicep Curls
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    angle = calculate_angle(shoulder, elbow, wrist)
                    if angle > 160:
                        in_down_position = True
                    elif angle < 30 and in_down_position:
                        rep_count += 1
                        in_down_position = False
                        last_command = "UP"

                elif workout_choice == 2:  # Squats
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                    angle = calculate_angle(hip, knee, ankle)
                    if angle < 60:
                        in_down_position = True
                    elif angle > 160 and in_down_position:
                        rep_count += 1
                        in_down_position = False
                        last_command = "UP"

                elif workout_choice == 3:  # Push-ups
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    angle = calculate_angle(shoulder, elbow, wrist)
                    if angle > 160:
                        in_down_position = True
                    elif angle < 90 and in_down_position:
                        rep_count += 1
                        in_down_position = False
                        last_command = "UP"

                elif workout_choice == 4:  # Plank
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                    angle_arm = calculate_angle(shoulder, elbow, wrist)
                    angle_leg = calculate_angle(hip, knee, ankle)
                    if 80 < angle_arm < 100 and angle_leg > 160:
                        if plank_start_time is None:
                            plank_start_time = time.time()
                        plank_duration = time.time() - plank_start_time
                        last_command = "HOLD"
                    else:
                        plank_start_time = None
                        plank_duration = 0
                        last_command = "ADJUST"

            # Draw info text
            status_text = f"Last Command: {last_command or 'N/A'}  "
            if workout_choice == 4:
                status_text += f"  Plank Duration: {plank_duration:.2f} s"
            else:
                status_text += f"  Rep Count: {rep_count}"

            image = cv2.putText(image, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            frame_display.image(rgb_image)

            if time.time() > end_time:
                break

    cap.release()
    return rep_count, plank_duration

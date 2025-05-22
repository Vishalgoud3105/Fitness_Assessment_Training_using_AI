#`components/camera.py`
import streamlit as st
import cv2
import mediapipe as mp

def run_camera():
    FRAME_WINDOW = st.image([])
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            st.warning("Failed to capture from webcam.")
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        FRAME_WINDOW.image(image)

    cap.release()
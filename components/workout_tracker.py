import pandas as pd
import time
import cv2
import mediapipe as mp
import numpy as np

#opencv
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def track_workout(workout_choice, end_time):
    cap = cv2.VideoCapture(0)
    rep_count = 0
    plank_duration = 0

    # Mouse callback function
    def close_camera(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            param['closed'] = True

    # Dictionary to keep track of the camera close status
    param = {'closed': False}

    # Create a window and set a mouse callback
    cv2.namedWindow('Workout Tracker')
    cv2.setMouseCallback('Workout Tracker', close_camera, param)

    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        last_command_time = {}
        workout_ended = False
        rep_count = 0
        last_command = None
        in_down_position = False
        plank_start_time = None
        plank_duration = 0
        
        while cap.isOpened() and not param['closed']:
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            landmarks = results.pose_landmarks

            if landmarks is not None:
                mp_drawing.draw_landmarks(image, landmarks, mp_pose.POSE_CONNECTIONS)

            try:
                landmarks = results.pose_landmarks.landmark

                # Your existing code with modifications
                if workout_choice == 1:  # Bicep Curls
                    shoulder_left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow_left = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist_left = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                                    landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    angle_left = calculate_angle(shoulder_left, elbow_left, wrist_left)

                    shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    elbow_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    wrist_right = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                    angle_right = calculate_angle(shoulder_right, elbow_right, wrist_right)

                    if angle_right > 160 and angle_left > 160:
                        last_command = "DOWN"
                        last_command_time['down_bicep'] = time.time()
                        in_down_position = True
                    elif angle_right < 30 and angle_left < 30 and in_down_position:
                        last_command = "UP"
                        rep_count += 1
                        last_command_time['up_bicep'] = time.time()
                        in_down_position = False

                elif workout_choice == 2:  # Squats
                    knee_left = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    hip_left = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    ankle_left = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    angle_left = calculate_angle(hip_left, knee_left, ankle_left)

                    knee_right = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    hip_right = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    ankle_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                    angle_right = calculate_angle(hip_right, knee_right, ankle_right)

                    if angle_left < 60 and angle_right < 60 and not in_down_position:
                        last_command = "DOWN"
                        last_command_time['down_squats'] = time.time()
                        in_down_position = True
                    elif angle_left > 160 and angle_right > 160 and in_down_position:
                        last_command = "UP"
                        rep_count += 1
                        last_command_time['up_squats'] = time.time()
                        in_down_position = False
                  
                elif workout_choice == 3:  # Push-ups
                    # Left arm
                    shoulder_left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow_left = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist_left = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    angle_left_arm = calculate_angle(shoulder_left, elbow_left, wrist_left)

                    # Right arm
                    shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    elbow_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    wrist_right = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                    angle_right_arm = calculate_angle(shoulder_right, elbow_right, wrist_right)

                    # Left leg
                    knee_left = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    hip_left = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    ankle_left = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    angle_left_leg = calculate_angle(hip_left, knee_left, ankle_left)

                    # Right leg
                    knee_right = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    hip_right = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    ankle_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                    angle_right_leg = calculate_angle(hip_right, knee_right, ankle_right)

                    if angle_left_arm > 160 and angle_right_arm > 160 and angle_left_leg > 160 and angle_right_leg > 160:
                        if not in_down_position:  # Ensure transition to "UP" position
                            last_command = "UP"
                            last_command_time['up_pushups'] = time.time()
                            in_down_position = False
                    elif angle_left_arm < 90 and angle_right_arm < 90:
                        if not in_down_position:  # Transition to "DOWN" position
                            last_command = "DOWN"
                            rep_count += 1
                            last_command_time['down_pushups'] = time.time()
                            in_down_position = True

                elif workout_choice == 4:  # Plank
                    # Left side
                    shoulder_left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow_left = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist_left = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    hip_left = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee_left = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    ankle_left = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    angle_left_arm = calculate_angle(shoulder_left, elbow_left, wrist_left)
                    angle_left_leg = calculate_angle(hip_left, knee_left, ankle_left)

                    # Right side
                    shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    elbow_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    wrist_right = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    hip_right = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    knee_right = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    ankle_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                    angle_right_arm = calculate_angle(shoulder_right, elbow_right, wrist_right)
                    angle_right_leg = calculate_angle(hip_right, knee_right, ankle_right)

                    if angle_left_arm > 80 and angle_left_arm < 100 and angle_right_arm > 80 and angle_right_arm < 100 and angle_left_leg > 160 and angle_right_leg > 160:
                        if plank_start_time is None:
                            plank_start_time = time.time()
                        plank_duration = time.time() - plank_start_time
                        last_command = "HOLD"
                    else:
                        last_command = "ADJUST"
                        plank_start_time = None
                        plank_duration = 0


                    print(f"Last Command: {last_command}, Plank Duration: {plank_duration:.2f}")

                key = cv2.waitKey(1) & 0xFF
                if key == ord('e'):
                    workout_ended = True

                if workout_choice == 4:  # Display plank duration for planks
                    cv2.putText(image, f'Last Command: {last_command}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(image, f'Plank Duration: {plank_duration:.2f} s', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                else:
                    cv2.putText(image, f'Last Command: {last_command}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(image, f'Rep Count: {rep_count}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                

                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                cv2.imshow('Workout Tracker', image)

            except Exception as e:
                print(e)

            if time.time() > end_time or workout_ended:
                break    

        cap.release()
        cv2.destroyAllWindows()

        return rep_count, plank_duration
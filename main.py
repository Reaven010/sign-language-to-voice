import cv2
import mediapipe as mp
import numpy as np
import joblib
from collections import deque

clf = joblib.load("isl_model.pkl")
encoder = joblib.load("isl_label_encoder.pkl")

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Webcam
cap = cv2.VideoCapture(0)

window_size = 5
predictions_window = deque(maxlen=window_size)

recognized_text = ""
current_sign = ""
hand_present = False  

print("Press ESC to exit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1) 
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        hand_present = True 

        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            pred = clf.predict([landmarks])[0]
            predictions_window.append(pred)

            smooth_pred = max(set(predictions_window), key=predictions_window.count)
            current_sign = encoder.inverse_transform([smooth_pred])[0]

            cv2.rectangle(frame, (40, 20), (400, 80), (0, 0, 0), -1)
            cv2.putText(frame, f"Current Sign: {current_sign}", (50, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    else:
        if hand_present and current_sign != "":
            recognized_text += current_sign
            current_sign = ""
        hand_present = False

    cv2.rectangle(frame, (40, 100), (800, 150), (0, 0, 0), -1)
    cv2.putText(frame, f"Text: {recognized_text}", (50, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)

    cv2.imshow("ISL Real-Time Recognition (String)", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
hands.close()

print("Final Recognized Text:", recognized_text)
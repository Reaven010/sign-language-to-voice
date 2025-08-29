import cv2 
import mediapipe as mp
import numpy as np
import joblib
from collections import deque
from sklearn.preprocessing import LabelEncoder

clf =joblib.load("isl_model.plk")
encoder = joblib.load("isl_label_encoder.pkl")

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.7)

cap =cv2.VideoCapture(0)

window_size =5
predictions_window = deque (maxlen=window_size)

recognized_text =""
last_sign=""
print("Press escape to exit . ")
while cap.isOpened():
    ret,frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame,1)
    image_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)

            landmarks=[]
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x,lm.y,lm.z])

            pred=clf.predict([landmarks])[0]
            predictions_window.append(pred)

            smooth_pred = max(set(predictions_window),key=predictions_window.count)
            sign=encoder.inverse_transform([smooth_pred])[0]

            if sign != last_sign:
                last_sign = sign
            cv2.putText(frame, f"sign : {sign}",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,255,0),3)
            cv2.putText(frame,f"Text : {recognized_text}",(50,100),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,0,0),2)
    cv2.imshow("Real Time recognistion (string)",frame)
    if cv2.waitkey(1)& 0xFF ==27:
        break
cap.release()
cv2.destroyAllWindows()
hands.close()

print("recognised text is : ",recognized_text)
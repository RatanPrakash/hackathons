import cv2
import mediapipe as mp
import time
import tensorflow as tf
from collections import deque

from utils import create_dataset, draw_landmarks, get_current_landmarks, predict_gesture

HOLD_TIME_THRESHOLD = 0.001
model_save_path = "main_model.hdf5"
mp_hands = mp.solutions.hands
model = tf.keras.models.load_model(model_save_path)
video = cv2.VideoCapture(0)

point_history = deque(maxlen=16)

hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.7, min_tracking_confidence=0.5)

first_run = True
set_gesture = None
debug = False

index = 0
while video.isOpened():
    success, true_image = video.read()
    image = cv2.flip(true_image, 1)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if not success:
        continue

    results = hands.process(image)
    image.flags.writeable = True

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):

            landmarks = get_current_landmarks(image, hand_landmarks)
            
            if debug:
                draw_landmarks(image, handedness, landmarks)
                # if handedness.classification[0].label == "Right":
                create_dataset(landmarks, "right", "data.csv") 
                index += 1                                                                                                                                                  
            else: 
                current_gesture = predict_gesture(model, landmarks)
                draw_landmarks(image, handedness, landmarks, set_gesture)
                if first_run:
                    set_gesture = current_gesture
                    hold_start_time = time.time()
                    prev_gesture = current_gesture
                    first_run = False
                    
                if current_gesture != prev_gesture:
                    hold_start_time = time.time()
                    prev_gesture = current_gesture
                    
                if time.time() - hold_start_time > HOLD_TIME_THRESHOLD:
                    set_gesture = current_gesture
                
                if set_gesture != current_gesture:
                    print(f"Next Change: Hold {current_gesture} for {round(HOLD_TIME_THRESHOLD - (time.time() - hold_start_time), 2)}s")
                print(f"label: {set_gesture}\n")

        if debug and index > 250:
            break
            
    else:
        print("Nothing Detected", set_gesture)
    
    cv2.imshow("x", cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    if cv2.waitKey(10) & 0xFF == 27:
        break


video.release()
cv2.destroyAllWindows()
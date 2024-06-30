import cv2
import mediapipe as mp

# Define the gesture recognition module using MediaPipe Hands
class GestureRecognition:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        
    def get_hand_landmarks(self, image, draw=True):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if draw:
                    mp.solutions.drawing_utils.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            
            return results.multi_hand_landmarks
    
    def classify_gesture(self, hand_landmarks):
        # Implement your gesture classification algorithm here
        # This could involve analyzing the position and orientation of the fingers, palm, and hand
        
        # For the sake of example, let's just assume the gesture is a "thumbs up" if the thumb is extended
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        thumb_x = thumb_tip.x * image_width
        thumb_y = thumb_tip.y * image_height
        
        if thumb_tip.visibility > 0.5:
            if thumb_x < image_width / 3:
                return "thumbs left"
            elif thumb_x > 2 * image_width / 3:
                return "thumbs right"
            else:
                return "thumbs up"
        
        return "no gesture"

# Set up the video capture device
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize the gesture recognition module
gesture_recognizer = GestureRecognition()

while True:
    # Capture a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        break
    
    # Get the dimensions of the video frame
    image_height, image_width, _ = frame.shape
    
    # Detect and draw hand landmarks
    hand_landmarks = gesture_recognizer.get_hand_landmarks(frame, draw=True)
    
    if hand_landmarks:
        # Classify the hand gesture
        gesture = gesture_recognizer.classify_gesture(hand_landmarks[0])
        cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Display the resulting image
    cv2.imshow("Hand Gesture Recognition", frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

class HandTracker:
    def __init__(self, model_path='hand_landmarker.task', max_hands=2, detection_con=0.5, track_con=0.5):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_con,
            min_hand_presence_confidence=track_con,
            running_mode=vision.RunningMode.IMAGE
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.results = None

    def find_hands(self, img, draw=True):
        # Convertir BGR a RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        # Detectar manos
        self.results = self.detector.detect(mp_image)
        
        if draw and self.results.hand_landmarks:
            for hand_landmarks in self.results.hand_landmarks:
                # Dibujar puntos manualmente ya que drawing_utils puede faltar
                for landmark in hand_landmarks:
                    x = int(landmark.x * img.shape[1])
                    y = int(landmark.y * img.shape[0])
                    cv2.circle(img, (x, y), 5, (0, 255, 0), cv2.FILLED)
        return img

    def get_landmarks(self, img):
        landmarks_list = []
        if self.results and self.results.hand_landmarks:
            for hand_landmarks in self.results.hand_landmarks:
                h, w, c = img.shape
                hand_data = []
                for id, lm in enumerate(hand_landmarks):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    hand_data.append((id, cx, cy))
                landmarks_list.append(hand_data)
        return landmarks_list

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        frame = tracker.find_hands(frame)
        lms = tracker.get_landmarks(frame)
        if lms:
            index_tip = lms[0][8]
            cv2.circle(frame, (index_tip[1], index_tip[2]), 15, (255, 0, 255), cv2.FILLED)
            
        cv2.imshow("Hand Tracker Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

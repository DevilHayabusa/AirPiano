import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=2, detection_con=0.7, track_con=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_con,
            min_tracking_confidence=track_con
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [8, 12, 16, 20] # Puntas: Índice, Medio, Anular, Meñique

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_landmarks(self, img):
        landmarks = []
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                h, w, c = img.shape
                hand_data = []
                for id, lm in enumerate(hand_lms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    hand_data.append((id, cx, cy))
                landmarks.append(hand_data)
        return landmarks

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.flip(frame, 1) # Espejo
        frame = tracker.find_hands(frame)
        lms = tracker.get_landmarks(frame)
        if lms:
            # Dibujar un círculo en la punta del índice de la primera mano
            index_tip = lms[0][8]
            cv2.circle(frame, (index_tip[1], index_tip[2]), 15, (255, 0, 255), cv2.FILLED)
            
        cv2.imshow("Hand Tracker Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

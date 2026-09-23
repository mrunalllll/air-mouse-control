import cv2
import mediapipe as mp
import pyautogui

screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(0)

hands = mp.solutions.hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

while True:

    _, img = cap.read()

    img = cv2.flip(img, 1)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        for hand in result.multi_hand_landmarks:

            index = hand.landmark[8]

            x = int(index.x * screen_w)
            y = int(index.y * screen_h)

            pyautogui.moveTo(x, y)

    cv2.imshow("Air Mouse", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
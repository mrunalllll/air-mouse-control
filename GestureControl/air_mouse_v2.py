import cv2
import mediapipe as mp
import pyautogui
import math
import time

# Screen Size
screen_w, screen_h = pyautogui.size()

# Camera
cap = cv2.VideoCapture(0)

# MediaPipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mpDraw = mp.solutions.drawing_utils

# Smooth Mouse Movement
prev_x = 0
prev_y = 0
smoothening = 5

# Cooldown
last_click_time = 0
click_delay = 1

while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    h, w, c = img.shape

    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            lmList = []

            for id, lm in enumerate(handLms.landmark):

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                lmList.append((cx, cy))

            # Index Finger Tip
            ix, iy = lmList[8]

            # Move Mouse
            mouse_x = screen_w / w * ix
            mouse_y = screen_h / h * iy

            curr_x = prev_x + (mouse_x - prev_x) / smoothening
            curr_y = prev_y + (mouse_y - prev_y) / smoothening

            pyautogui.moveTo(curr_x, curr_y)

            prev_x = curr_x
            prev_y = curr_y

            # Thumb Tip
            tx, ty = lmList[4]

            # Middle Finger Tip
            mx, my = lmList[12]

            # Distance Thumb-Index
            click_distance = math.hypot(ix - tx, iy - ty)

            # Distance Thumb-Middle
            right_click_distance = math.hypot(mx - tx, my - ty)

            current_time = time.time()

            # Left Click
            if click_distance < 35:

                if current_time - last_click_time > click_delay:

                    pyautogui.click()

                    print("LEFT CLICK")

                    last_click_time = current_time

            # Right Click
            if right_click_distance < 35:

                if current_time - last_click_time > click_delay:

                    pyautogui.rightClick()

                    print("RIGHT CLICK")

                    last_click_time = current_time

            # Two Finger Scroll Mode
            index_up = lmList[8][1] < lmList[6][1]
            middle_up = lmList[12][1] < lmList[10][1]

            if index_up and middle_up:

                center_y = (lmList[8][1] + lmList[12][1]) // 2

                if center_y < 180:

                    pyautogui.scroll(50)

                    cv2.putText(
                        img,
                        "SCROLL UP",
                        (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                elif center_y > 300:

                    pyautogui.scroll(-50)

                    cv2.putText(
                        img,
                        "SCROLL DOWN",
                        (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2
                    )

            mpDraw.draw_landmarks(
                img,
                handLms,
                mpHands.HAND_CONNECTIONS
            )

    cv2.putText(
        img,
        "AIR MOUSE V2",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )

    cv2.imshow("Air Mouse V2", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
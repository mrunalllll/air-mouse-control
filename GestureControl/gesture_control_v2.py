import cv2
import mediapipe as mp
import math
import time
import pyautogui
import screen_brightness_control as sbc

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ==========================================
# AUDIO SETUP
# ==========================================

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)

volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]

# ==========================================
# MEDIAPIPE SETUP
# ==========================================

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mpDraw = mp.solutions.drawing_utils

# ==========================================
# CAMERA
# ==========================================

cap = cv2.VideoCapture(0)

last_action_time = 0
cooldown = 2
previous_x = 0

# ==========================================
# FIST DETECTION
# ==========================================

def is_fist(lmList):
    tips = [8, 12, 16, 20]
    folded = 0

    for tip in tips:
        if lmList[tip][1] > lmList[tip - 2][1]:
            folded += 1

    return folded >= 4

# ==========================================
# MAIN LOOP
# ==========================================

while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    h, w, c = img.shape

    if results.multi_hand_landmarks and results.multi_handedness:

        for handLms, handedness in zip(
            results.multi_hand_landmarks,
            results.multi_handedness
        ):

            label = handedness.classification[0].label

            lmList = []

            for lm in handLms.landmark:

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                lmList.append((cx, cy))

            if len(lmList) < 21:
                continue

            thumb_x, thumb_y = lmList[4]
            index_x, index_y = lmList[8]

            distance = math.hypot(
                index_x - thumb_x,
                index_y - thumb_y
            )

            # ==================================
            # RIGHT HAND = VOLUME
            # ==================================

            if label == "Right":

                vol = (distance - 20) / (250 - 20)
                vol = max(0, min(vol, 1))

                volume.SetMasterVolumeLevel(
                    volMin + (volMax - volMin) * vol,
                    None
                )

                cv2.putText(
                    img,
                    f"Volume: {int(vol*100)}%",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                cv2.rectangle(img, (20, 80), (50, 300), (0,255,0), 2)

                bar = int(
                    300 - (vol * 220)
                )

                cv2.rectangle(
                    img,
                    (20, bar),
                    (50, 300),
                    (0,255,0),
                    cv2.FILLED
                )

            # ==================================
            # LEFT HAND = BRIGHTNESS
            # ==================================

            elif label == "Left":

                bright = int(
                    max(
                        0,
                        min(
                            100,
                            (distance - 20) * 100 / 230
                        )
                    )
                )

                sbc.set_brightness(bright)

                cv2.putText(
                    img,
                    f"Brightness: {bright}%",
                    (20, 350),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,255,0),
                    2
                )

                cv2.rectangle(
                    img,
                    (80,80),
                    (110,300),
                    (255,255,0),
                    2
                )

                bar2 = int(
                    300 - (bright * 220 / 100)
                )

                cv2.rectangle(
                    img,
                    (80,bar2),
                    (110,300),
                    (255,255,0),
                    cv2.FILLED
                )

            # ==================================
            # PLAY / PAUSE
            # ==================================

            if is_fist(lmList):

                current_time = time.time()

                if current_time - last_action_time > cooldown:

                    pyautogui.press("playpause")

                    last_action_time = current_time

                    cv2.putText(
                        img,
                        "PLAY / PAUSE",
                        (200, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,255,255),
                        3
                    )

            # ==================================
            # SWIPE GESTURES
            # ==================================

            current_x = lmList[8][0]

            if current_x - previous_x > 120:

                current_time = time.time()

                if current_time - last_action_time > cooldown:

                    pyautogui.press("nexttrack")

                    last_action_time = current_time

                    cv2.putText(
                        img,
                        "NEXT TRACK",
                        (200,100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,255,0),
                        3
                    )

            elif previous_x - current_x > 120:

                current_time = time.time()

                if current_time - last_action_time > cooldown:

                    pyautogui.press("prevtrack")

                    last_action_time = current_time

                    cv2.putText(
                        img,
                        "PREVIOUS TRACK",
                        (200,100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,0,255),
                        3
                    )

            previous_x = current_x

            # ==================================
            # DRAW
            # ==================================

            cv2.line(
                img,
                (thumb_x, thumb_y),
                (index_x, index_y),
                (255, 0, 255),
                3
            )

            cv2.circle(
                img,
                (thumb_x, thumb_y),
                10,
                (255,0,255),
                cv2.FILLED
            )

            cv2.circle(
                img,
                (index_x, index_y),
                10,
                (255,0,255),
                cv2.FILLED
            )

            mpDraw.draw_landmarks(
                img,
                handLms,
                mpHands.HAND_CONNECTIONS
            )

    cv2.putText(
        img,
        "ESC = EXIT",
        (10, h - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )

    cv2.imshow(
        "Gesture Control V2.0",
        img
    )

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
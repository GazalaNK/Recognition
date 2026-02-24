import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    h, w, c = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:

            lm = hand.landmark

            # Landmark coordinates
            x1, y1 = int(lm[4].x*w), int(lm[4].y*h)   # Thumb tip
            x2, y2 = int(lm[8].x*w), int(lm[8].y*h)   # Index tip
            x3, y3 = int(lm[12].x*w), int(lm[12].y*h) # Middle tip

            # Distance between thumb and index
            distance = math.hypot(x2-x1, y2-y1)

            # Draw circles
            cv2.circle(img,(x1,y1),10,(255,0,0),-1)
            cv2.circle(img,(x2,y2),10,(255,0,0),-1)

            # Gesture 1: Pinch → Mouse Click
            if distance < 30:
                pyautogui.click()
                cv2.putText(img,"Click",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

            # Gesture 2: Thumb up → Volume Up
            if y1 < y2:
                pyautogui.press("volumeup")
                cv2.putText(img,"Volume Up",(50,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

            # Gesture 3: Thumb down → Volume Down
            if y1 > y2:
                pyautogui.press("volumedown")
                cv2.putText(img,"Volume Down",(50,150),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

            # Gesture 4: Fist → Pause/Play
            if abs(y2 - y3) < 10:
                pyautogui.press("space")
                cv2.putText(img,"Play/Pause",(50,200),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

            mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture Computer Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
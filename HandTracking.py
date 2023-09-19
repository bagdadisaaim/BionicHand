import math

import cv2
import mediapipe as mp
import time
import cvzone


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


prevTime = 0
currentTime = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLMS in results.multi_hand_landmarks:
            #print(handLMS.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP], results.multi_handedness)
            mpDraw.draw_landmarks(img, handLMS, mpHands.HAND_CONNECTIONS)

            xIndexFingerDistance = handLMS.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].x - handLMS.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP].x
            yIndexFingerDistance = handLMS.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y - handLMS.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP].y
            zIndexFingerDistance = handLMS.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].z - handLMS.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP].z
            indexDistance = math.sqrt(math.pow(xIndexFingerDistance, 2) + math.pow(yIndexFingerDistance, 2) + math.pow(zIndexFingerDistance, 2))
            print(indexDistance)





    currentTime = time.time()
    fps = 1/(currentTime - prevTime)
    prevTime = currentTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)


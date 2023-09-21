import math

import cv2
import mediapipe as mp
import uuid
import os
import numpy as np
import time
import cvzone

from google.protobuf.json_format import MessageToDict


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils


prevTime = 0
currentTime = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for i in results.multi_handedness:
            # Return whether it is Right or Left Hand
            label = MessageToDict(i)[
                'classification'][0]['label']

            if label == 'Right':
                for handLMS in results.multi_hand_landmarks:
                    mpDraw.draw_landmarks(img, handLMS, mpHands.HAND_CONNECTIONS)

                    wristLMK = handLMS.landmark[mpHands.HandLandmark.WRIST]
                    bottomIndexLMK = handLMS.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP]
                    topIndexLMK = handLMS.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]

                    # calculating angle for index finger
                    indexA = np.array([float(wristLMK.x), float(wristLMK.y)])  # First coord
                    indexB = np.array([float(bottomIndexLMK.x), float(bottomIndexLMK.y)])  # Second coord
                    indexC = np.array([float(topIndexLMK.x), float(topIndexLMK.y)])  # Third coord
                    radians = np.arctan2(indexC[1] - indexB[1], indexC[0] - indexB[0]) - np.arctan2(indexA[1] - indexB[1], indexA[0] - indexB[0])
                    indexAngle = float(np.abs(radians * 180.0 / np.pi))
                    if indexAngle > 180:
                        indexAngle = 360 - indexAngle
                        print("index finger angle:", indexAngle)
                    else:
                        print("index finger angle:", indexAngle)

                    #middle finger
                    middleA = np.array([float(wristLMK.x), float(wristLMK.y)])  # First coord
                    middleB = np.array([float(bottomIndexLMK.x), float(bottomIndexLMK.y)])  # Second coord
                    middleC = np.array([float(topIndexLMK.x), float(topIndexLMK.y)])  # Third coord
                    radians = np.arctan2(middleC[1] - middleB[1], middleC[0] - middleB[0]) - np.arctan2(middleA[1] - middleB[1], middleA[0] - middleB[0])
                    middleAngle = float(np.abs(radians * 180.0 / np.pi))
                    if middleAngle > 180:
                        middleAngle = 360 - middleAngle
                        print("Middle finger angle:", middleAngle)
                    else:
                        print("middle finger angle:", middleAngle)









    currentTime = time.time()
    fps = 1/(currentTime - prevTime)
    prevTime = currentTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)


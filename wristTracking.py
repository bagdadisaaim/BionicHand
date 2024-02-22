import cv2
import mediapipe as mp
import numpy as np
import time
import serial 
from google.protobuf.json_format import MessageToDict
import matplotlib.pyplot as plt



cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

prevTime = 0
currentTime = 0

while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
    results = hands.process(imgRGB)

    def findwristangle(angle):
        if len(str(angle)) == 1:
            angle = '00' + str(angle)
            return(angle)
        elif len(str(angle)) == 2:
            angle = '0' + str(angle)
            return(angle)
        else:
            return(angle)

    if results.multi_hand_landmarks:
        for i in results.multi_handedness:
            # Return whether it is Right or Left Hand
            label = MessageToDict(i)[
                'classification'][0]['label']

            if label == 'Right':
                for handLMS in results.multi_hand_landmarks:
                    mpDraw.draw_landmarks(img, handLMS, mpHands.HAND_CONNECTIONS)

                    palm1 = handLMS.landmark[mpHands.HandLandmark.PINKY_MCP]
                    palm2 = handLMS.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP]
                    palm3 = handLMS.landmark[mpHands.HandLandmark.PINKY_MCP]
                    palmA = np.array([float(palm1.x), float(palm1.z)])
                    palmB = np.array([float(palm2.x), float(palm2.z)])
                    palmC = np.array([float(palm3.x + 1), float(palm3.z)])

                    palmRadians = np.arctan2(palmC[1] - palmB[1], palmC[0] - palmB[0]) - np.arctan2(palmA[1] - palmB[1], palmA[0] - palmB[0])
                    palmAngle = float(np.abs(palmRadians * 180.0 / np.pi))

                    if palmAngle > 180 and palmAngle <= 270:
                        palmAngle = 360 - palmAngle
                        print(findwristangle(int(palmAngle)))
                    elif  palmAngle < 0 and palmAngle > 270:
                        palmAngle = 360 - palmAngle
                        print(findwristangle(int(palmAngle)))
                    else :
                        print(findwristangle(int(palmAngle)))




    currentTime = time.time()
    fps = 1/(currentTime - prevTime)
    prevTime = currentTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)

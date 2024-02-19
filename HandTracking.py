import math

import cv2
import mediapipe as mp
import uuid
import os
import numpy as np
import time
import cvzone
import serial 
from google.protobuf.json_format import MessageToDict
import pyfirmata
from pyfirmata import Arduino, util, SERVO



cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.00001)
mpDraw = mp.solutions.drawing_utils

mySerial = serial.Serial(port='COM5')


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

                    bottomMiddleLMK = handLMS.landmark[mpHands.HandLandmark.MIDDLE_FINGER_MCP]
                    topMiddleLMK = handLMS.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP]

                    bottomRingLMK = handLMS.landmark[mpHands.HandLandmark.RING_FINGER_MCP]
                    topRingLMK = handLMS.landmark[mpHands.HandLandmark.RING_FINGER_TIP]

                    bottomPinkyLMK = handLMS.landmark[mpHands.HandLandmark.PINKY_MCP]
                    topPinkyLMK = handLMS.landmark[mpHands.HandLandmark.PINKY_TIP]

                    bottomThumbLMK = handLMS.landmark[mpHands.HandLandmark.THUMB_MCP]
                    topThumbLMK = handLMS.landmark[mpHands.HandLandmark.THUMB_TIP]
                    middleThumbLMK = handLMS.landmark[mpHands.HandLandmark.THUMB_IP]

                    fingerpositions = "$"


                    def findquadrant(angle):
                        if angle >=0 and angle<= 55:
                            return 1
                        if angle >=56 and angle<= 165:
                            return 2
                        if angle >=166 and angle<= 180:
                            return 3

                        
                    def findthumbquadrant(angle):
                        if angle >=0 and angle<= 55:
                            return 1
                        if angle >=56 and angle<= 165:
                            return 2
                        if angle >=166 and angle<= 180:
                            return 3


                    # calculating angle for index finger
                    indexA = np.array([float(wristLMK.x), float(wristLMK.y)])  # First coord
                    indexB = np.array([float(bottomIndexLMK.x), float(bottomIndexLMK.y)])  # Second coord
                    indexC = np.array([float(topIndexLMK.x), float(topIndexLMK.y)])  # Third coord
                    indexRadians = np.arctan2(indexC[1] - indexB[1], indexC[0] - indexB[0]) - np.arctan2(indexA[1] - indexB[1], indexA[0] - indexB[0])
                    indexAngle = float(np.abs(indexRadians * 180.0 / np.pi))
                    if indexAngle > 180:
                        indexAngle = 360 - indexAngle
                        #print("index finger angle:", int(indexAngle))
                        fingerpositions = fingerpositions + str(findquadrant(int(indexAngle)))
                        #mySerial.write(str(fingerpositions).encode())
                    else:
                        #print("index finger angle:", int(indexAngle))
                        fingerpositions = fingerpositions + str(findquadrant(int(indexAngle)))
                        #mySerial.write(str(fingerpositions).encode())

                    
                    #middle finger
                    middleA = np.array([float(wristLMK.x), float(wristLMK.y)])  # First coord
                    middleB = np.array([float(bottomMiddleLMK.x), float(bottomMiddleLMK.y)])  # Second coord
                    middleC = np.array([float(topMiddleLMK.x), float(topMiddleLMK.y)])  # Third coord
                    middleRadians = np.arctan2(middleC[1] - middleB[1], middleC[0] - middleB[0]) - np.arctan2(middleA[1] - middleB[1], middleA[0] - middleB[0])
                    middleAngle = float(np.abs(middleRadians * 180.0 / np.pi))
                    if middleAngle > 180:
                        middleAngle = 360 - middleAngle
                        #print("middle finger angle:", int(middleAngle))
                        fingerpositions = fingerpositions + str(findquadrant(int(middleAngle)))
                        #mySerial.write(str(fingerpositions).encode())
                    else:
                        #print("middle finger angle:", int(middleAngle))
                        fingerpositions = fingerpositions + str(findquadrant(int(middleAngle)))
                        #mySerial.write(str(fingerpositions).encode())

                    #ring finger
                    ringA = np.array([float(wristLMK.x), float(wristLMK.y)])  # First coord
                    ringB = np.array([float(bottomRingLMK.x), float(bottomRingLMK.y)])  # Second coord
                    ringC = np.array([float(topRingLMK.x), float(topRingLMK.y)])  # Third coord
                    ringRadians = np.arctan2(ringC[1] - ringB[1], ringC[0] - ringB[0]) - np.arctan2(ringA[1] - ringB[1], ringA[0] - ringB[0])
                    ringAngle = float(np.abs(ringRadians * 180.0 / np.pi))
                    if ringAngle > 180:
                        ringAngle = 360 - ringAngle
                        #print("ring finger angle:", int(ringAngle))
                        fingerpositions = fingerpositions +  str(findquadrant(int(ringAngle)))
                        #mySerial.write(str(fingerpositions).encode())
                    else:
                        #print("ring finger angle:", int(ringAngle))
                        fingerpositions = fingerpositions +  str(findquadrant(int(ringAngle)))
                        #mySerial.write(str(fingerpositions).encode())

                    #pinky finger
                    pinkyA = np.array([float(wristLMK.x), float(wristLMK.y)])  # First coord
                    pinkyB = np.array([float(bottomPinkyLMK.x), float(bottomPinkyLMK.y)])  # Second coord
                    pinkyC = np.array([float(topPinkyLMK.x), float(topPinkyLMK.y)])  # Third coord
                    pinkyRadians = np.arctan2(pinkyC[1] - pinkyB[1], pinkyC[0] - pinkyB[0]) - np.arctan2(pinkyA[1] - pinkyB[1], pinkyA[0] - pinkyB[0])
                    pinkyAngle = float(np.abs(pinkyRadians * 180.0 / np.pi))
                    if pinkyAngle > 180:
                        pinkyAngle = 360 - pinkyAngle
                        #print("pinky finger angle:", int(pinkyAngle))
                        fingerpositions = fingerpositions + str(findquadrant(int(pinkyAngle)))
                        #mySerial.write(str(fingerpositions).encode())
                    else:
                        #print("pinky finger angle:", int(pinkyAngle))
                        fingerpositions = fingerpositions +  str(findquadrant(int(pinkyAngle)))
                        #mySerial.write(str(fingerpositions).encode())

                    #thumb finger
                    thumbA = np.array([float(wristLMK.x), float(wristLMK.y)])  # First coord
                    thumbB = np.array([float(bottomThumbLMK.x), float(bottomThumbLMK.y)])  # Second coord
                    thumbC = np.array([float(topThumbLMK.x), float(topThumbLMK.y)])  # Third coord
                    thumbRadians1 = np.arctan2(thumbC[1] - thumbB[1], thumbC[0] - thumbB[0]) - np.arctan2(thumbA[1] - middleB[1], thumbA[0] - thumbB[0])
                    thumbAngle1 = float(np.abs(thumbRadians1 * 180.0 / np.pi))
                    if thumbAngle1 > 180:
                        thumbAngle1 = 360 - thumbAngle1
                        #print("thumb finger angle:", int(thumbAngle1))
                        fingerpositions = fingerpositions + str(findthumbquadrant(int(thumbAngle1)))
                        #mySerial.write(str(fingerpositions).encode())
                    else:
                        #print("thumb finger angle:", int(thumbAngle1))
                        fingerpositions = fingerpositions +  str(findthumbquadrant(int(thumbAngle1)))
                        #mySerial.write(str(fingerpositions).encode())

                    print(str(fingerpositions))
                    mySerial.write(str(fingerpositions).encode())
                    time.sleep(0.5)
                    fingerpositions = "$"



    currentTime = time.time()
    fps = 1/(currentTime - prevTime)
    prevTime = currentTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)


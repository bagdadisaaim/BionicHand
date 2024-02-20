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

    if results.multi_hand_landmarks:
        for i in results.multi_handedness:
            # Return whether it is Right or Left Hand
            label = MessageToDict(i)[
                'classification'][0]['label']

            if label == 'Right':
                for handLMS in results.multi_hand_landmarks:
                    mpDraw.draw_landmarks(img, handLMS, mpHands.HAND_CONNECTIONS)

                    palm1 = handLMS.landmark[mpHands.HandLandmark.WRIST]
                    palm2 = handLMS.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP]
                    palm3 = handLMS.landmark[mpHands.HandLandmark.PINKY_MCP]
                    palmA = np.array([float(palm1.x), float(palm1.y)])
                    palmB = np.array([float(palm2.x), float(palm2.y)])
                    palmC = np.array([float(palm3.x), float(palm3.y)])

                    points = np.asarray([palmA, palmB, palmC])

                    normal_vector = np.cross(points[2] - points[0], points[1] - points[2])
                    normal_vector /= np.linalg.norm(normal_vector)

                    mpDraw.draw_axis(img, 0, 0)



    currentTime = time.time()
    fps = 1/(currentTime - prevTime)
    prevTime = currentTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)

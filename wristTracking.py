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


cap = cv2.VideoCapture(0)

mpPose = mp.solutions.pose
wrist = mpPose.Pose(max_num_poses=1)
mpDraw = mp.solutions.drawing_utils


prevTime = 0
currentTime = 0

while True:

    #def sendToArduino(wristPositions):
     #   cmd=('Wrist position: ' + str(wristPositions[0]))
      #  cmd=cmd+'\r'
       # ser.write(cmd.encode())


    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = wrist.process(imgRGB)

        
    if results.multi_pose_landmarks:
        for i in results.multi_handedness:
            # Return whether it is Right or Left Hand
            label = MessageToDict(i)[
                'classification'][0]['label']

            if label == 'Right':
                for handLMS in results.multi_pose_landmarks:
                    mpDraw.draw_landmarks(img, handLMS, mpPose.POSE_CONNECTIONS)


    currentTime = time.time()
    fps = 1/(currentTime - prevTime)
    prevTime = currentTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)

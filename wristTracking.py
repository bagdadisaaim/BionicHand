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
import matplotlib.pyplot as plt


cap = cv2.VideoCapture(0)

# Initialize mediapipe pose class.
mp_pose = mp.solutions.pose

# Setup the Pose function for images - independently for the images standalone processing.
pose_image = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

# Setup the Pose function for videos - for video processing.
pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.7,
                          min_tracking_confidence=0.7)

# Initialize mediapipe drawing class - to draw the landmarks points.
mp_drawing = mp.solutions.drawing_utils

prevTime = 0
currentTime = 0




while True:

    def detectPose(image_pose, pose, draw=False, display=False):
    
        original_image = image_pose.copy()
        
        image_in_RGB = cv2.cvtColor(image_pose, cv2.COLOR_BGR2RGB)
        
        resultant = pose.process(image_in_RGB)

        if resultant.pose_landmarks and draw:    

            mp_drawing.draw_landmarks(image=original_image, landmark_list=resultant.pose_landmarks,
                                    connections=mp_pose.POSE_CONNECTIONS,
                                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,255),
                                                                                thickness=3, circle_radius=3),
                                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(49,125,237),
                                                                                thickness=2, circle_radius=2))


    image_path = cap.read()
    output = cv2.imread(image_path)
    detectPose(output, pose_image, draw=True, display=True)
    


    currentTime = time.time()
    fps = 1/(currentTime - prevTime)
    prevTime = currentTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)

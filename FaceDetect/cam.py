# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 09:15:17 2022

@author: ruchi
"""

# ******************************************************************
#
# Simple_camera_connect is a script that connects to a USB camera
#
# ******************************************************************



# ******* IMPORTS **********
import cv2 as cv
# **************************




# The number in VideoCapture represents which usb device will be connected
# 0 usually defaults to the host camera. If you are using a laptop then 0
# will be the devices default camera
cap = cv.VideoCapture(1)



# we check camera connection. If you enter this statement you will have to
# change the number in VideoCapture() from above
if not cap.isOpened():
    print("Cannot open camera")
    exit()



while True:



    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        break
    
    
    
    cv.namedWindow('frame', cv.WINDOW_NORMAL)
    cv.imshow('frame', frame)
    
    
    
    # if 'q' is pressed close the window and end the program
    if cv.waitKey(1) == ord('q'):
        break



cap.release()
cv.destroyAllWindows()
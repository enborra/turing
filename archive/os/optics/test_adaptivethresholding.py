import cv2
import numpy as np
from matplotlib import pyplot as plt


hand_cascade = cv2.CascadeClassifier('algorithms/haarcascade_hand_alt.xml')

cap = cv2.VideoCapture(0)

###
### Loop infinitely to project camera analysis onto output display window
###

while 1:
    is_frame_available, source_frame = cap.read()

    img = source_frame
    # img = cv2.imread('hand.jpg',0)
    img = cv2.medianBlur(img,5)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

    th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    # images = [img, th1, th2, th3]

    cv2.imshow('img', th2)

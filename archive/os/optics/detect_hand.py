import numpy as np
import cv2

hand_cascade = cv2.CascadeClassifier('algorithms/haarcascade_hand_alt.xml')



###
### Capture image frame from camera for processing
###

cap = cv2.VideoCapture(0)

###
### Loop infinitely to project camera analysis onto output display window
###

while 1:
    is_frame_available, source_frame = cap.read()

    curr_frame = source_frame
    # curr_frame = cv2.cvtColor(source_frame, cv2.COLOR_BGR2GRAY)
    curr_frame = cv2.cvtColor(source_frame, cv2.COLOR_BGR2YUV)
    curr_frame[:,:,0] = cv2.equalizeHist(curr_frame[:,:,0])
    curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_YUV2BGR)

    curr_frame = cv2.medianBlur(curr_frame,5)
    curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)


    # ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

    # curr_frame = cv2.adaptiveThreshold(curr_frame,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    # th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)


    # curr_frame = cv2.equalizeHist(curr_frame)

    try:
        hands = hand_cascade.detectMultiScale(
            curr_frame,
            scaleFactor=1.12,
            minNeighbors=25,
            minSize=(100, 100),

            # maxSize=(150, 100),
        )

        if len(hands) > 0:
            for( hand_x, hand_y, hand_w, hand_h ) in hands:
                cv2.rectangle(
                    curr_frame,
                    (hand_x, hand_y),
                    (hand_x+hand_w, hand_y+hand_h),
                    (255,255,0),
                    1
                )


    except Exception, e:
        print 'ERROR: ' + str(e)

    cv2.imshow('img', curr_frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

import numpy as np
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('algorithms/haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier('algorithms/haarcascade_face.xml')

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
# eye_cascade = cv2.CascadeClassifier('algorithms/haarcascade_eye.xml')
# eye_cascade = cv2.CascadeClassifier('algorithms/haarcascade_mcs_eyepair_big.xml')
eye_cascade = cv2.CascadeClassifier('algorithms/haarcascade_mcs_eyepair_small.xml')

# smile_cascade = cv2.CascadeClassifier('algorithms/haarcascade_smile.xml')

cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    curr_frame = gray

    try:
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(curr_frame,(x,y),(x+w,y+h),(255,0,0),2)

            cv2.circle(
                curr_frame,
                (x+(w/2), y+(h/2)),
                40,
                (255, 255, 255),
                2
            )

            # roi_gray = gray[y:y+h, x:x+w]
            # roi_color = img[y:y+h, x:x+w]
            #
            # try:
            #     eyes = eye_cascade.detectMultiScale(curr_frame)
            #
            #     for (ex,ey,ew,eh) in eyes:
            #         cv2.rectangle(curr_frame,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            # except Exception, e:
            #     pass



            # smiles = smile_cascade.detectMultiScale(
            #     contrst,
            #     # scaleFactor=1.3,
            #     # minNeighbors=30,
            # )
            #
            # for( x, y, w, h) in smiles:
            #     cv2.rectangle(curr_frame, (x,y), (x+w, y+h), (255,255,0), 2)

    except Exception, e:
        pass

    cv2.imshow('img',curr_frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

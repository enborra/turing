import cv2
import sys

faceCascade = cv2.CascadeClassifier('algorithms/haarcascade_face.xml')
# faceCascade = cv2.CascadeClassifier('algorithms/haarcascade_mcs_eyepair_big.xml')
# faceCascade = cv2.CascadeClassifier('algorithms/haarcascade_mcs_eyepair_small.xml')
# faceCascade = cv2.CascadeClassifier('algorithms/haarcascade_frontalface_alt_tree.xml')
# faceCascade = cv2.CascadeClassifier('algorithms/haarcascade_frontalface_alt.xml')
# faceCascade = cv2.CascadeClassifier('algorithms/haarcascade_eye_tree_eyeglasses.xml')

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.equalizeHist(gray)

    faces = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(250, 250),
        # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 255, 255), 4)

        # roi_gray = gray[y:y+h, x:x+w]
        # roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(gray)

        # for (ex,ey,ew,eh) in eyes:
        #     cv2.rectangle(gray,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)

    # smiles = smile_cascade.detectMultiScale(
    #     gray,
    #     scaleFactor=1.1,
    #     minNeighbors=10,
    #     minSize=(100,50)
    # )
    #
    # for( x, y, w, h) in smiles:
    #     cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 255, 0), 1)

    # Display the resulting frame
    cv2.imshow('Video', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

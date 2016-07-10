import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('algorithms/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('algorithms/haarcascade_mcs_eyepair_small.xml')
nose_cascade = cv2.CascadeClassifier('algorithms/nose.xml')
smile_cascade = cv2.CascadeClassifier('algorithms/haarcascade_smile.xml')



###
### Capture image frame from camera for processing
###

cap = cv2.VideoCapture(0)

###
### Loop infinitely to project camera analysis onto output display window
###

while 1:
    is_frame_available, source_frame = cap.read()

    gray = cv2.cvtColor(source_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    curr_frame = gray

    try:
        faces = face_cascade.detectMultiScale3(
            curr_frame,
            scaleFactor=1.05,
            minNeighbors=5,
            minSize=(140, 140),
            flags = cv2.CASCADE_SCALE_IMAGE,
            outputRejectLevels = True
        )

        face_rects = faces[0]
        face_neighbours = faces[1]
        face_weights = faces[2]

        source_width, source_height, source_channels = source_frame.shape


        ###
        ### Find the face rect with the highest associated probability weight
        ###

        winning_index = 0
        winning_prob = 0.0

        if len(face_rects)>1:
            for i in range(0,len(face_rects)):
                print '......rect: ' + str(face_rects[i]) + ', and probability: ' + str(face_weights[i])

                if float(face_weights[i]) > winning_prob:
                    winning_prob = face_weights[i]
                    winning_index = i

        ###
        ### Draw the match rectangle onto the source video frame
        ###

        for (face_x, face_y, face_w, face_h) in faces[winning_index]:
            # if weights[0][0] > -2:

            print 'Face size: ' + str(face_w) + ' x ' + str(face_h) + ', weights: ' + str(face_weights[0][0])
            print 'Face position: x:' + str(face_x) + ', y: ' + str(face_y)

            cv2.rectangle(
                source_frame,
                (face_x, face_y),
                (face_x+face_w, face_y+face_h),
                (255,255,255),
                1
            )

            ###
            ### When selecting a subregion, y is the first input range, then x.
            ### For some reason.
            ###

            face_frame = source_frame[
                face_y:face_y+face_h,
                face_x:face_x+face_w
            ]

            cv2.rectangle(
                face_frame,             # canvas
                (4, 4),                 # start corner x,y
                (face_w-4, face_h-4),   # end corner x,y
                (255, 0, 0),            # color
                1                       # line thickness
            )

            ###
            ### DETECT NOSES
            ###

            noses = nose_cascade.detectMultiScale(
                face_frame,
                scaleFactor=1.05,
                minNeighbors=5,
                minSize=(80, 40),
                maxSize=(150, 100),
            )

            for( nose_x, nose_y, nose_w, nose_h ) in noses:
                cv2.rectangle(
                    face_frame,
                    (nose_x, nose_y),
                    (nose_x+nose_w, nose_y+nose_h),
                    (255, 255, 0),
                    1,

                )

                # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

            # # Detect eyes
            #
            # roi_gray = gray[
            #     face_y : face_y + face_h,
            #     face_x : face_x + face_w
            # ]
            #
            # roi_color = source_frame[
            #     face_y : face_y + face_h,
            #     face_x : face_x + face_w
            # ]
            #
            # eyes = eye_cascade.detectMultiScale(
            #     source_frame,
            #     scaleFactor=1.05,
            #     minNeighbors=5
            # )
            #
            # for (ex,ey,ew,eh) in eyes:
            #     cv2.rectangle(source_frame,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            #
            #     print 'found eye.'


            # face_area_gray = gray[ face_x:face_x+face_w, face_y:face_y+face_h ]
            # face_area_color = source_frame[ face_x:face_x+face_w, face_y:face_y+face_h ]
            #
            # try:
            #     eyes = eye_cascade.detectMultiScale(
            #         face_area_color,
            #         # scaleFactor=1.3,
            #         # minNeighbors=5
            #     )
            #
            #     for (ex,ey,ew,eh) in eyes:
            #         cv2.rectangle(source_frame, (ex,ey),(ex+ew,ey+eh),(255,255,255),2)
            #
            #         # cv2.circle(
            #         #     source_frame,
            #         #     (ex, ey),
            #         #     20,
            #         #     (255, 255, 255),
            #         #     2
            #         # )
            #
            # except Exception, e:
            #     print 'ERROR' + str(e)



            # smiles = smile_cascade.detectMultiScale(
            #     contrst,
            #     # scaleFactor=1.3,
            #     # minNeighbors=30,
            # )
            #
            # for( x, y, w, h) in smiles:
            #     cv2.rectangle(curr_frame, (x,y), (x+w, y+h), (255,255,0), 2)

    except Exception, e:
        print 'ERROR: ' + str(e)

    cv2.imshow('img',source_frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

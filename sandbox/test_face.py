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

    # gray = cv2.cvtColor(source_frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.equalizeHist(gray)

    curr_frame = source_frame

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
            found_nose = False
            found_eyes = False
            found_mouth = False

            print 'Face size: ' + str(face_w) + ' x ' + str(face_h) + ', weights: ' + str(face_weights[0][0])
            print 'Face position: x:' + str(face_x) + ', y: ' + str(face_y)

            # cv2.rectangle(
            #     source_frame,
            #     (face_x, face_y),
            #     (face_x+face_w, face_y+face_h),
            #     (255,255,255),
            #     1
            # )

            ###
            ### When selecting a subregion, y is the first input range, then x.
            ### For some reason.
            ###

            face_frame = curr_frame[
                face_y:face_y+face_h,
                face_x:face_x+face_w
            ]

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

            if len(noses) > 0:
                found_nose = True


            ### Detect eyes

            # roi_gray = gray[
            #     face_y : face_y + face_h,
            #     face_x : face_x + face_w
            # ]

            # roi_color = source_frame[
            #     face_y : face_y + face_h,
            #     face_x : face_x + face_w
            # ]

            eyes = eye_cascade.detectMultiScale(
                face_frame,
                scaleFactor=1.05,
                minNeighbors=5
            )

            if len(eyes) > 0:
                found_eyes = True


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

            smiles = smile_cascade.detectMultiScale(
                face_frame,
                scaleFactor=1.03,
                minNeighbors=30,
                minSize=(80, 40),
                maxSize=(400, 200),
            )

            mouth_candidate = None
            mouth_candidate_y = 0

            if len(smiles) > 0:
                print 'Smiles: ' + str(len(smiles))
                print smiles

                for( x, y, w, h ) in smiles:
                    _is_new_candidate = False


                    if y > (face_h/3):
                        if mouth_candidate is None:
                            _is_new_candidate = True

                        else:
                            if (y > mouth_candidate_y):
                                _is_new_candidate = True

                    if _is_new_candidate:
                        found_mouth = True

                        mouth_candidate_y = y
                        mouth_candidate = {
                            'x': x,
                            'y': y,
                            'w': w,
                            'h': h
                        }

                print 'Winner: ' + str(mouth_candidate)

            if found_nose or found_eyes or found_mouth:
                ### Draw face marker box

                cv2.rectangle(
                    face_frame,             # canvas
                    (0, 0),                 # start corner x,y
                    (face_w-1, face_h-1),   # end corner x,y
                    (255, 255, 255),        # color
                    1                       # line thickness
                )

                ### Draw nose yellow marker box

                for( nose_x, nose_y, nose_w, nose_h ) in noses:
                    cv2.circle(
                        face_frame,
                        (nose_x+(nose_w/2), nose_y+(nose_h/2)),
                        40,
                        (0, 255, 255),
                        1,
                    )

                ### Draw eyes green marker box

                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(
                        face_frame,
                        (ex,ey),
                        (ex+ew,ey+eh),
                        (0,255,0),
                        2
                    )

                ### Draw smile teal marker box

                if found_mouth:
                    cv2.rectangle(
                        face_frame,
                        (mouth_candidate['x'], mouth_candidate['y']),
                        (mouth_candidate['x']+mouth_candidate['w'], mouth_candidate['y']+mouth_candidate['h']),
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

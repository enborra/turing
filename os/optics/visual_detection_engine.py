import os
import numpy as np
import cv2


class VisualDetectionEngine(object):
    _camera_source = None
    _cascades = None

    _is_capturing_active = False
    _current_source_frame = None
    _current_working_frame = None
    _current_detected_faces = None


    # ----------------------------------------------
    # PUBLIC METHODS
    # ----------------------------------------------


    def __init__(self):
        algorithm_dir = os.path.realpath(__file__ + '/../algorithms')

        self._cascades = {
            'face': cv2.CascadeClassifier(algorithm_dir+'/haarcascade_frontalface_default.xml'),
            'eye': cv2.CascadeClassifier(algorithm_dir+'/haarcascade_mcs_eyepair_small.xml'),
            'nose': cv2.CascadeClassifier(algorithm_dir+'/nose.xml'),
            'mouth': cv2.CascadeClassifier(algorithm_dir+'/haarcascade_smile.xml'),
        }

        print os.path.realpath(__file__ + '/../')

        print '[TURING.OS.OPTICS] Starting video capture..'
        self._camera_source = cv2.VideoCapture(0)
        print '[TURING.OS.OPTICS] Video capture enabled.'


    def get_capture(self):
        is_frame_available, self._current_source_frame = self._camera_source.read()
        self._current_working_frame = self._current_source_frame

        try:
            self._current_detected_faces = self._detect_faces()
            source_width, source_height, source_channels = self._current_source_frame.shape

        except Exception, e:
            print 'ERROR: ' + str(e)

    def get_continuous_capture(self):
        self._is_capturing_active = True

        while self._is_capturing_active:
            self.get_capture()
            img = self._composite_output_frame()

            if len(self._current_detected_faces) > 0:
                # Determining rough face distance

                cv2.putText(self._current_working_frame, str(self._current_detected_faces[0]['w']) + ':' + str(self._current_detected_faces[0]['h']), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)

            cv2.imshow('img', self._current_working_frame)

            # if self._current_detected_faces:
            #     print 'FACES: ' + str(len(self._current_detected_faces))

            if (cv2.waitKey(30) & 0xff) == 27:
                self._is_capturing_active = False

        self._camera_source.release()
        cv2.destroyAllWindows()

    def track_continuous_object(self):
        self._is_capture_active = True
        is_face_found = False

        while self._is_capture_active and not is_face_found:
            self.get_capture()
            img = self._composite_output_frame()

            cv2.imshow('img', self._current_working_frame)

            if len(self._current_detected_faces) > 0:
                is_face_found = True

        if is_face_found:
            print "FOUND A FACE. TIME TO TRACK IT."

        r = self._current_detected_faces[0]['y']
        h = self._current_detected_faces[0]['h']
        c = self._current_detected_faces[0]['x']
        w = self._current_detected_faces[0]['w']

        # r = 300
        # h = 200
        # c = 300
        # w = 200

        track_window = (c, r, w, h)

        # set up the ROI for tracking
        roi = self._current_working_frame[r:r+h, c:c+w]
        hsv_roi =  cv2.cvtColor(self._current_working_frame, cv2.COLOR_BGR2HSV)





        # mask_color_sensitivity = 15
        # lower_white = np.array([0, 0, 255-mask_color_sensitivity])
        # upper_white = np.array([180, mask_color_sensitivity, 255])
        #
        # mask = cv2.inRange(
        #     hsv_roi,
        #     lower_white,
        #     upper_white,
        # )






        # mask_color_sensitivity = 15
        # lower_mask_color_a = (0, 100, 100)
        # upper_mask_color_a = (mask_color_sensitivity, 255, 255)
        #
        # lower_mask_color_b = (180-mask_color_sensitivity, 100, 100)
        # upper_mask_color_b = (180, 255, 255)

        # mask_a = cv2.inRange(
        #     hsv_roi,
        #     np.array(lower_mask_color_a),
        #     np.array(upper_mask_color_a)
        # )
        #
        # mask_b = cv2.inRange(
        #     hsv_roi,
        #     np.array(lower_mask_color_b),
        #     np.array(upper_mask_color_b)
        # )
        #
        # mask = cv2.bitwise_or(mask_a, mask_b)



        avg_color_row = np.average(roi, axis=0)
        avg_color = np.average(avg_color_row, axis=0)

        print avg_color


        mask = cv2.inRange(
            roi,
            np.array(avg_color*0.5),
            np.array(avg_color*1.15)
        )



        avg_color = np.uint8(avg_color)
        average_color_img = np.array([[avg_color]*100]*100, np.uint8)
        cv2.imshow('hsv_color_mask', average_color_img)




        roi_hist = cv2.calcHist([roi],[0], mask, [180], [0,180])
        cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

        # Setup the termination criteria, either 10 iteration or move by at least 1 pt
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

        while True:
            old_img = self._current_working_frame

            self.get_capture()

            new_img = cv2.GaussianBlur(self._current_working_frame, (13, 13), 0)
            # new_img = self._current_working_frame

            hsv = cv2.cvtColor(new_img, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

            ret, track_window = cv2.meanShift(dst, track_window, term_crit)

            x, y, w, h = track_window

            img2 = cv2.rectangle(new_img, (x, y), (x+w, y+h), (255,255,0), 2)
            cv2.imshow('img', new_img)

            hrm = cv2.bitwise_and(hsv, hsv, mask=mask)
            cv2.imshow('mask', hrm)


            k = cv2.waitKey(60) & 0xff

            if k == 27:
                break









        self._camera_source.release()
        cv2.destroyAllWindows()


    # ----------------------------------------------
    # INTERNAL METHODS
    # ----------------------------------------------


    def _detect_faces(self):
        found_faces = []

        face_data_arrays = self._cascades['face'].detectMultiScale3(
            self._current_working_frame,
            scaleFactor=1.05,
            minNeighbors=5,
            minSize=(140, 140),
            flags=cv2.CASCADE_SCALE_IMAGE,
            outputRejectLevels=True,
        )

        if len(face_data_arrays) > 0:
            face_datasets = {
                'rects': face_data_arrays[0],
                'neighbors': face_data_arrays[1],
                'weights': face_data_arrays[2],
            }

            for (face_x, face_y, face_w, face_h) in face_datasets['rects']:
                curr_face = {
                    'x': 0, 'y': 0, 'w': 0, 'h': 0,
                    'frame': None,
                    'face': None,
                    'nose': None,
                    'eyes': None,
                    'mouth': None,
                }

                ### When selecting a subregion, y is the first input range, then x.
                ### For some reason.

                curr_face['x'] = face_x
                curr_face['y'] = face_y
                curr_face['w'] = face_w
                curr_face['h'] = face_h

                curr_face['frame'] = self._current_working_frame[
                    face_y:face_y+face_h,
                    face_x:face_x+face_w
                ]

                curr_face['nose'] = self._detect_nose(
                    curr_face['frame'],
                    self._cascades['nose']
                )

                curr_face['eyes'] = self._detect_eyes(
                    curr_face['frame'],
                    self._cascades['eye']
                )
                curr_face['mouth'] = self._detect_mouth(
                    curr_face['frame'],
                    self._cascades['mouth']
                )

                if curr_face['mouth'] or curr_face['eyes'] or curr_face['mouth']:
                    found_faces.append(curr_face)

        return found_faces

    def _detect_nose(self, frame, cascade_algorithm):
        return cascade_algorithm.detectMultiScale(
            frame,
            scaleFactor=1.05,
            minNeighbors=5,
            minSize=(80, 40),
            maxSize=(150, 100),
        )

    def _detect_eyes(self, frame, cascade_algorithm):
        return cascade_algorithm.detectMultiScale(
            frame,
            scaleFactor=1.05,
            minNeighbors=5
        )

    def _detect_mouth(self, frame, cascade_algorithm):
        frame_width, frame_height = frame.shape[:2]
        mouth_candidate = None
        mouth_candidate_y = 0

        mouths = cascade_algorithm.detectMultiScale(
            frame,
            scaleFactor=1.03,
            minNeighbors=30,
            minSize=(80, 40),
            maxSize=(400, 200),
        )

        if len(mouths) > 0:
            for( x, y, w, h ) in mouths:
                _is_new_candidate = False

                if y > (frame_height/3):
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

        return mouth_candidate

    def _composite_output_frame(self):
        if self._current_detected_faces:
            for f in self._current_detected_faces:
                ### Draw face marker box

                cv2.rectangle(
                    f['frame'],             # canvas
                    (0, 0),                 # start corner x,y
                    (f['w']-1, f['h']-1),   # end corner x,y
                    (255, 255, 255),        # color
                    1                       # line thickness
                )

                ### Draw mouth frame marker box

                cv2.rectangle(
                    f['frame'],
                    (f['mouth']['x'], f['mouth']['y']),
                    (f['mouth']['x'] + f['mouth']['w'], f['mouth']['y'] + f['mouth']['h']),
                    (255,255,0),
                    1
                )

                ### Draw eyes green marker box

                for (ex,ey,ew,eh) in f['eyes']:
                    cv2.rectangle(
                        f['frame'],
                        (ex,ey),
                        (ex+ew,ey+eh),
                        (0,255,0),
                        2
                    )

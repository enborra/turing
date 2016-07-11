import numpy as np
import cv2


class VisualDetectionEngine(object):
    _camera_source = None
    _cascades = {
        'face': cv2.CascadeClassifier('algorithms/haarcascade_frontalface_default.xml'),
        'eye': cv2.CascadeClassifier('algorithms/haarcascade_mcs_eyepair_small.xml'),
        'nose': cv2.CascadeClassifier('algorithms/nose.xml'),
        'mouth': cv2.CascadeClassifier('algorithms/haarcascade_smile.xml'),
    }

    _is_capturing_active = False
    _current_source_frame = None
    _current_working_frame = None
    _current_detected_faces = None


    def __init__(self):
        self._camera_source = cv2.VideoCapture(0)

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

            cv2.imshow('img', self._current_working_frame)

            if (cv2.waitKey(30) & 0xff) == 27:
                self._is_capturing_active = False

        self._camera_source.release()
        cv2.destroyAllWindows()


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
        ### Draw face marker box

        for f in self._current_detected_faces:
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

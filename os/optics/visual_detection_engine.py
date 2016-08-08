import os
import numpy as np
import cv2
import time
from datetime import datetime

from core import BaseController
from storage import Storable


class VisualDetectionEngine(BaseController):
    _environment = None
    _camera_source = None
    _cascades = None

    _is_capturing_active = False
    _current_source_frame = None
    _current_working_frame = None
    _current_detected_faces = None

    _tracking_state = None
    _track_window = None
    _hist = None
    _is_face_isolated = False

    _iteration_count_colortrack = 0
    _time_last_face_find = None


    # ----------------------------------------------
    # PUBLIC METHODS
    # ----------------------------------------------


    def __init__(self, environment=None):
        BaseController.__init__(self)

        self._class_output_id = 'turing.os.optics'

        self._environment = environment

        algorithm_dir = os.path.realpath(__file__ + '/../algorithms')

        self._cascades = {
            'face': cv2.CascadeClassifier(algorithm_dir+'/haarcascade_frontalface_default.xml'),
            'eye': cv2.CascadeClassifier(algorithm_dir+'/haarcascade_mcs_eyepair_small.xml'),
            'nose': cv2.CascadeClassifier(algorithm_dir+'/nose.xml'),
            'mouth': cv2.CascadeClassifier(algorithm_dir+'/haarcascade_smile.xml'),
        }

        if self._environment == 'onboard':
            self.output('Running (onboard)')
        else:
            self.output('Running (simulated)')


        self.output('Starting video capture')
        self._camera_source = cv2.VideoCapture(0)
        self.output('Video capture enabled')

        self._tracking_state = None
        self._track_window = None
        self._hist = None

        if self._environment == 'simulated':
            cv2.namedWindow('hist')
            cv2.namedWindow('face')
            cv2.namedWindow('camshift')
            cv2.namedWindow('hsv')

            cv2.moveWindow('face', 40, 500)
            cv2.moveWindow('mask', 40, 700)
            cv2.moveWindow('hsv', 40, 800)
            cv2.moveWindow('camshift', 450, 100)
            cv2.moveWindow('hist', 450, 850)

        self._tracking_state = 0


    def get_capture(self):
        is_frame_available, self._current_source_frame = self._camera_source.read()
        self._current_working_frame = self._current_source_frame

        # try:
        #     self._current_detected_faces = self._detect_faces()
        #     source_width, source_height, source_channels = self._current_source_frame.shape
        #
        # except Exception, e:
        #     print 'ERROR: ' + str(e)

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
            self.output('FOUND A FACE. TIME TO TRACK IT.')

        r = self._current_detected_faces[0]['y']
        h = self._current_detected_faces[0]['h']
        c = self._current_detected_faces[0]['x']
        w = self._current_detected_faces[0]['w']

        # r = 300
        # h = 200
        # c = 300
        # w = 200

        self._track_window = (c, r, w, h)

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

            ret, self._track_window = cv2.meanShift(dst, self._track_window, term_crit)

            x, y, w, h = self._track_window

            img2 = cv2.rectangle(new_img, (x, y), (x+w, y+h), (255,255,0), 2)
            cv2.imshow('img', new_img)

            hrm = cv2.bitwise_and(hsv, hsv, mask=mask)
            cv2.imshow('mask', hrm)


            k = cv2.waitKey(60) & 0xff

            if k == 27:
                break









        self._camera_source.release()
        cv2.destroyAllWindows()


    def loop(self):
        if self._is_face_isolated:
            self._loop_isolated_face_track()
        else:
            self._loop_detect_face()

    def _loop_detect_face(self):
        self.get_capture()

        tracking_status = 'searching'

        s = Storable('turing')
        s.upsert('active_state', {'key': 'system_state', 'val': 'searching_for_person'})

        if self._environment == 'simulated':
            cv2.imshow('camshift', self._current_source_frame)

        self._current_detected_faces = self._cascades['face'].detectMultiScale(
            self._current_source_frame,
            scaleFactor=1.05,
            minNeighbors=5,
            minSize=(100, 100),
            flags = cv2.CASCADE_SCALE_IMAGE,
        )

        if len(self._current_detected_faces) > 0:
            self._is_face_isolated = True

            s = Storable('turing')
            s.upsert('active_state', {'key': 'system_state', 'val': 'tracking_person'})

            self._time_last_face_find = datetime.now()
            tracking_status = 'face_found'
            x, y, w, h = self._current_detected_faces[0]

            start_y = y + (h/10)
            end_y = y + h - (h/1.4)
            start_x = x + (w/4)
            end_x = x + w - (w/4)

            face_capture = self._current_source_frame[ y : y+h, x : x+w]
            face_capture_color = self._current_source_frame[ start_y : end_y, start_x : end_x ]

            face_capture_color_blur = face_capture_color

            lowest_h = 65
            highest_h = 256

            lowest_saturation = 55
            highest_saturation = 256

            lowest_intensity = 0
            highest_intensity = 256

            x, y, w, h = self._current_detected_faces[0]
            self._track_window = (x, y, x+w, y+h)
            iteration_count_colortrack = 0
            is_still_tracking = True


    def _loop_isolated_face_track(self):
        lowest_h = 65
        highest_h = 256

        lowest_saturation = 55
        highest_saturation = 256

        lowest_intensity = 0
        highest_intensity = 256

        time_last_face_find = datetime.now()
        tracking_status = 'face_found'
        x, y, w, h = self._current_detected_faces[0]

        start_y = y + (h/10)
        end_y = y + h - (h/1.4)
        start_x = x + (w/4)
        end_x = x + w - (w/4)

        self.get_capture()
        self._current_source_frame = cv2.GaussianBlur(self._current_source_frame, (31, 31), 0)

        vis = self._current_source_frame.copy()
        hsv = cv2.cvtColor(self._current_source_frame, cv2.COLOR_BGR2HSV)

        lower_bound = np.array((lowest_h, lowest_saturation, lowest_intensity))
        upper_bound = np.array((highest_h, highest_saturation, highest_intensity))

        # Bitmask out anything not in the min/max HSV range of the
        # captured face frame region

        mask = cv2.inRange(hsv, np.array((5.0, 60.0, 100.0)), np.array((100.0, 200.0, 255.0)))
        # mask = cv2.inRange(hsv, lower_bound, upper_bound)

        hsv_roi = hsv[y:y+h, x:x+w]
        mask_roi = mask[y:y+h, x:x+w]

        # hsv_roi = hsv
        # mask_roi = mask

        hist_bins = 120
        hist_range = [0, 180]

        # If grayscale img input, channel is 0.
        # If color img input, channels 0, 1, 2 map to blue, green, and red

        hist_channel = 0
        self._hist = None

        self._hist = cv2.calcHist( [hsv_roi], [hist_channel], mask_roi, [hist_bins], hist_range )
        self._hist = cv2.normalize(self._hist, self._hist, 0, 200, cv2.NORM_MINMAX);

        self._hist = self._hist.reshape(-1)

        if self._environment == 'simulated':
            cv2.imshow('mask', mask_roi)
            cv2.imshow('hsv', hsv_roi)

            self._show_hist()

        vis_roi = vis[y:y+h, x:x+w]
        # vis[mask == 0] = 0

        back_projection_channel = 0
        back_projection_range = [0, 180]
        back_projection_scale = 1

        prob = cv2.calcBackProject(
            [hsv],
            [back_projection_channel],
            self._hist,
            back_projection_range,
            back_projection_scale
        )

        prob &= mask
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

        track_box, self._track_window = cv2.CamShift(prob, self._track_window, term_crit)

        # Draw original face discovery bounds

        cv2.rectangle(
            self._current_source_frame,         # canvas
            (x, y),                             # start corner x,y
            (x+w-1, y+h-1),                     # end corner x,y
            (1, 1, 1),                          # color
            1                                   # line thickness
        )

        try:
            cv2.ellipse(self._current_source_frame, track_box, (150, 150, 150), 1)

            start_pos, end_pos, rotation = track_box
            center_x, center_y = start_pos
            width_detect, height_detect = end_pos

            start_x = int(center_x - (width_detect/2))
            start_y = int(center_y - (height_detect/2))
            end_x = int(center_x + (width_detect/2))
            end_y = int(center_y + (height_detect/2))

            seconds_tracking = (datetime.now() - self._time_last_face_find).total_seconds()

            frame_height, frame_width = self._current_source_frame.shape[:2]

            if width_detect < 100:
                self._is_face_isolated = False

            if seconds_tracking < 2:
                if (start_x > (x+100)) or (start_x < x-100):
                    self._is_face_isolated = False

                if width_detect > ((x+w)*2):
                    self._is_face_isolated = False

            if height_detect > frame_height:
                self._is_face_isolated = False

            cv2.rectangle(
                self._current_source_frame,     # canvas
                (start_x, start_y),             # start corner x,y
                (end_x, end_y),                 # end corner x,y
                (255, 255, 255),                # color
                2                               # line thickness
            )

            cv2.circle(self._current_source_frame, (30, 35), 10, (255, 255, 255), -1)
            cv2.putText(self._current_source_frame, ('Tracking for ' + str(int(seconds_tracking)) + ' seconds'), (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255))

            # print 'Tracking for ' + str(int(seconds_tracking)) + ' seconds'

        except Exception, e:
            self.output('Had a problem: ' + str(e))

        if self._environment == 'simulated':
            cv2.imshow('camshift', self._current_source_frame)

        if self._iteration_count_colortrack > 100:
            self._iteration_count_colortrack = 0
            self._is_face_isolated = False

        else:
            self._iteration_count_colortrack += 1







    def track_face(self):
        if self._environment == 'simulated':
            cv2.namedWindow('hist')
            cv2.namedWindow('face')
            cv2.namedWindow('camshift')
            cv2.namedWindow('hsv')

            cv2.moveWindow('face', 40, 500)
            cv2.moveWindow('mask', 40, 700)
            cv2.moveWindow('hsv', 40, 800)
            cv2.moveWindow('camshift', 450, 100)
            cv2.moveWindow('hist', 450, 850)

        time_last_face_find = None
        tracking_status = ''

        while True:
            _tracking_state = None
            _track_window = None
            _hist = None

            try:
                is_face_found = False

                tracking_status = 'searching'

                while not is_face_found:
                    self.get_capture()

                    if self._environment == 'simulated':
                        cv2.imshow('camshift', self._current_source_frame)

                    self._current_detected_faces = self._cascades['face'].detectMultiScale(
                        self._current_source_frame,
                        scaleFactor=1.05,
                        minNeighbors=5,
                        minSize=(100, 100),
                        flags = cv2.CASCADE_SCALE_IMAGE,
                    )

                    if len(self._current_detected_faces)  > 0:
                        is_face_found = True

                time_last_face_find = datetime.now()

                tracking_status = 'face_found'

                x, y, w, h = self._current_detected_faces[0]
                hrm = 4

                start_y = y + (h/10)
                end_y = y + h - (h/1.4)
                start_x = x + (w/4)
                end_x = x + w - (w/4)

                face_capture = self._current_source_frame[ y : y+h, x : x+w]
                face_capture_color = self._current_source_frame[ start_y : end_y, start_x : end_x ]

                face_capture_color_blur = face_capture_color

                lowest_h = 65
                highest_h = 256

                lowest_saturation = 55
                highest_saturation = 256

                lowest_intensity = 0
                highest_intensity = 256

                x, y, w, h = self._current_detected_faces[0]
                self._track_window = (x, y, x+w, y+h)
                iteration_count_colortrack = 0
                is_still_tracking = True

                while (iteration_count_colortrack < 500) and is_still_tracking:
                    time.sleep(0.01)

                    _, self._current_source_frame = self._camera_source.read()
                    self._current_source_frame = cv2.GaussianBlur(self._current_source_frame, (31, 31), 0)

                    vis = self._current_source_frame.copy()
                    hsv = cv2.cvtColor(self._current_source_frame, cv2.COLOR_BGR2HSV)

                    lower_bound = np.array((lowest_h, lowest_saturation, lowest_intensity))
                    upper_bound = np.array((highest_h, highest_saturation, highest_intensity))

                    # Bitmask out anything not in the min/max HSV range of the
                    # captured face frame region

                    mask = cv2.inRange(hsv, np.array((5.0, 60.0, 100.0)), np.array((100.0, 200.0, 255.0)))
                    # mask = cv2.inRange(hsv, lower_bound, upper_bound)

                    hsv_roi = hsv[y:y+h, x:x+w]
                    mask_roi = mask[y:y+h, x:x+w]

                    # hsv_roi = hsv
                    # mask_roi = mask

                    hist_bins = 120
                    hist_range = [0, 180]

                    # If grayscale img input, channel is 0.
                    # If color img input, channels 0, 1, 2 map to blue, green, and red

                    hist_channel = 0
                    hist = None

                    hist = cv2.calcHist( [hsv_roi], [hist_channel], mask_roi, [hist_bins], hist_range )
                    hist = cv2.normalize(hist, hist, 0, 200, cv2.NORM_MINMAX);


                    if self._environment == 'simulated':
                        cv2.imshow('mask', mask_roi)
                        cv2.imshow('hsv', hsv_roi)

                    # if self.hist is None:
                    self._hist = hist.reshape(-1)

                    self._show_hist()

                    vis_roi = vis[y:y+h, x:x+w]
                    vis[mask == 0] = 0

                    back_projection_channel = 0
                    back_projection_range = [0, 180]
                    back_projection_scale = 1

                    prob = cv2.calcBackProject(
                        [hsv],
                        [back_projection_channel],
                        self._hist,
                        back_projection_range,
                        back_projection_scale
                    )

                    prob &= mask
                    term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

                    track_box, self._track_window = cv2.CamShift(prob, self._track_window, term_crit)

                    # Draw original face discovery bounds

                    cv2.rectangle(
                        self._current_source_frame,       # canvas
                        (x, y),           # start corner x,y
                        (x+w-1, y+h-1),   # end corner x,y
                        (1, 1, 1),        # color
                        1                 # line thickness
                    )

                    try:
                        cv2.ellipse(self._current_source_frame, track_box, (150, 150, 150), 1)

                        start_pos, end_pos, rotation = track_box
                        center_x, center_y = start_pos
                        width_detect, height_detect = end_pos

                        start_x = int(center_x - (width_detect/2))
                        start_y = int(center_y - (height_detect/2))
                        end_x = int(center_x + (width_detect/2))
                        end_y = int(center_y + (height_detect/2))

                        seconds_tracking = (datetime.now() - time_last_face_find).total_seconds()

                        frame_height, frame_width = self._current_source_frame.shape[:2]

                        if width_detect < 100:
                            is_still_tracking = False

                        if seconds_tracking < 2:
                            if (start_x > (x+100)) or (start_x < x-100):
                                is_still_tracking = False

                            if width_detect > ((x+w)*2):
                                is_still_tracking = False

                        if height_detect > frame_height:
                            is_still_tracking = False

                        cv2.rectangle(
                            self._current_source_frame,             # canvas
                            (start_x, start_y),     # start corner x,y
                            (end_x, end_y),         # end corner x,y
                            (255, 255, 255),        # color
                            2                       # line thickness
                        )

                        cv2.circle(self._current_source_frame, (30, 35), 10, (255, 255, 255), -1)
                        cv2.putText(self._current_source_frame, ('Tracking for ' + str(int(seconds_tracking)) + ' seconds'), (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255))

                    except Exception, e:
                        self.output('ERROR: ' + str(e))

                    if self._environment == 'simulated':
                        cv2.imshow('camshift', self._current_source_frame)

                    if (0xFF & cv2.waitKey(5)) == 27:
                        break

                    iteration_count_colortrack += 1


            except Exception, e:
                self.output('ERROR: ' + str(e))




    # ----------------------------------------------
    # INTERNAL METHODS
    # ----------------------------------------------


    def _show_hist(self):
        bin_count = self._hist.shape[0]
        bin_w = 8
        img = np.zeros((256, bin_count*bin_w, 3), np.uint8)

        for i in xrange(bin_count):
            h = int(self._hist[i])
            cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)

        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        cv2.imshow('hist', img)





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

import numpy as np
import cv2


face_cascade = cv2.CascadeClassifier('algorithms/haarcascade_frontalface_default.xml')


class App(object):
    frame = None
    cam = None
    # drag_start = None
    # selection = None
    show_backproj = None
    tracking_state = None
    track_window = None
    hist = None


    def __init__(self, video_src):
        self.cam = cv2.VideoCapture(0)

        ret, self.frame = self.cam.read()
        cv2.namedWindow('camshift')
        # cv2.setMouseCallback('camshift', self.onmouse)

        self.selection = None
        self.drag_start = None
        self.tracking_state = 0
        self.show_backproj = False

    def show_hist(self):
        bin_count = self.hist.shape[0]
        bin_w = 8
        img = np.zeros((256, bin_count*bin_w, 3), np.uint8)

        for i in xrange(bin_count):
            h = int(self.hist[i])
            cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)

        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        cv2.imshow('hist', img)

    def run(self):
        cv2.namedWindow('hist')
        cv2.namedWindow('face')
        cv2.namedWindow('camshift')
        cv2.namedWindow('hsv')

        cv2.moveWindow('face', 40, 500)
        cv2.moveWindow('mask', 40, 700)
        cv2.moveWindow('hsv', 40, 800)
        cv2.moveWindow('camshift', 450, 100)
        cv2.moveWindow('hist', 450, 850)

        import time

        while True:
            self.face = None
            self.frame = None
            show_backproj = None
            tracking_state = None
            track_window = None
            hist = None

            try:
                is_face_found = False
                self.face = None

                print 'Trying to find new face...'

                # self.frame = cv2.GaussianBlur(self.frame, (13, 13), 0)

                while not is_face_found:
                    ret, self.frame = self.cam.read()

                    cv2.imshow('camshift', self.frame)

                    faces = face_cascade.detectMultiScale(
                        self.frame,
                        scaleFactor=1.05,
                        minNeighbors=5,
                        minSize=(140, 140),
                        flags = cv2.CASCADE_SCALE_IMAGE,
                        # outputRejectLevels = True
                    )

                    print 'Searched, parsing...'

                    if len(faces)  > 0:
                        is_face_found = True

                        self.face = faces[0]



                print 'found face. lets track it.'

                x, y, w, h = self.face
                hrm = 4

                start_y = y + (h/10)
                end_y = y + h - (h/1.4)
                start_x = x + (w/4)
                end_x = x + w - (w/4)

                face_capture = self.frame[ y : y+h, x : x+w]
                face_capture_color = self.frame[ start_y : end_y, start_x : end_x ]

                i = 0
                blur_amount = 5

                # face_capture_color_blur = cv2.GaussianBlur(face_capture_color, (blur_amount,blur_amount), 0)
                face_capture_color_blur = 


                lowest_h = -1
                highest_h = -1
                lowest_saturation = -1
                highest_saturation = -1
                lowest_intensity = -1
                highest_intensity = -1

                for col in face_capture_color_blur:
                    for row in col:
                        hue = row[0]
                        saturation = row[1]
                        intensity = row[2]

                        if (lowest_h == -1) or (hue < lowest_h):
                            lowest_h = hue

                        elif (highest_h == -1) or (hue > highest_h):
                            highest_h = hue


                        if (lowest_saturation == -1) or (saturation < lowest_saturation):
                            lowest_saturation = saturation

                        elif (highest_saturation == -1) or (saturation > highest_saturation):
                            highest_saturation = saturation

                        if (lowest_intensity == -1) or (intensity < lowest_intensity):
                            lowest_intensity = intensity

                        if (highest_intensity == -1) or (intensity > highest_intensity):
                            highest_intensity = intensity


                print 'Lowest hsv is: ' + str(lowest_h) + ', ' + str(lowest_saturation) + ', ' + str(lowest_intensity)
                print 'Highest hsv is: ' + str(highest_h) + ', ' + str(highest_saturation) + ', ' + str(highest_intensity)
                print '...'


                x, y, w, h = self.face
                self.track_window = (x, y, x+w, y+h)

                while i < 20:
                    ret, self.frame = self.cam.read()
                    # self.frame = cv2.GaussianBlur(self.frame, (13, 13), 0)

                    vis = self.frame.copy()
                    hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

                    # Bitmask out anything not in the min/max HSV range of the
                    # captured face frame region

                    mask = cv2.inRange(
                        hsv,
                        np.array((lowest_h, lowest_saturation, lowest_intensity)),
                        np.array((highest_h, highest_saturation, highest_intensity))
                    )

                    cv2.imshow('face', face_capture_color_blur)

                    hsv_roi = hsv[y:y+h, x:x+w]
                    mask_roi = mask[y:y+h, x:x+w]

                    # hsv_roi = hsv
                    # mask_roi = mask

                    hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [256], [0, 256] )
                    # cv2.normalize(hist, hist, 100, 190, cv2.NORM_MINMAX);

                    cv2.imshow('mask', mask_roi)
                    cv2.imshow('hsv', hsv_roi)

                    # if self.hist is None:
                    self.hist = hist.reshape(-1)

                    self.show_hist()

                    vis_roi = vis[y:y+h, x:x+w]
                    # cv2.bitwise_not(vis_roi, vis_roi)
                    vis[mask == 0] = 0




                    self.selection = None

                    prob = cv2.calcBackProject([hsv], [0], self.hist, [0, 180], 1)
                    prob &= mask

                    term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

                    track_box, self.track_window = cv2.CamShift(prob, self.track_window, term_crit)

                    cv2.rectangle(
                        self.frame,             # canvas
                        (x, y),                 # start corner x,y
                        (x+w-1, y+h-1),   # end corner x,y
                        (1, 1, 1),        # color
                        1                       # line thickness
                    )

                    if self.show_backproj:
                        vis[:] = prob[...,np.newaxis]

                    try:
                        cv2.ellipse(self.frame, track_box, (0, 0, 255), 2)

                        start_pos, end_pos, rotation = track_box
                        start_x, start_y = start_pos
                        end_x, end_y = end_pos

                        cv2.rectangle(
                            self.frame,             # canvas
                            (0, 0),                 # start corner x,y
                            (20, 20),   # end corner x,y
                            (255, 255, 255),        # color
                            2                       # line thickness
                        )

                    except:
                        print 'Had a problem: ' + str(track_box)

                    cv2.imshow('camshift', self.frame)

                    ch = 0xFF & cv2.waitKey(5)

                    if ch == 27:
                        break

                    if ch == ord('b'):
                        self.show_backproj = not self.show_backproj

                    i += 1
            except Exception, e:
                print 'digger: ' + str(e)

        cv2.destroyAllWindows()


if __name__ == '__main__':
    import sys
    try:
        video_src = sys.argv[1]

    except:
        video_src = 0

    print __doc__

    App(video_src).run()

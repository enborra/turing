import numpy as np
import cv2

from common import clock, draw_str
import video

class App(object):

    def __init__(self, video_src):

        if video_src == "webcam":
            self.cam = video.create_capture(0)

        else:
            self.vidFile = cv.CaptureFromFile('sources/' + video_src + '.mp4')
            self.vidFrames = int(cv.GetCaptureProperty(self.vidFile, cv.CV_CAP_PROP_FRAME_COUNT))

        self.cascade_fn = "haarcascades/haarcascade_frontalface_default.xml"
        self.cascade = cv2.CascadeClassifier(self.cascade_fn)

        self.left_eye_fn = "haarcascades/haarcascade_eye.xml"
        self.left_eye = cv2.CascadeClassifier(self.left_eye_fn)

        self.mouth_fn = "haarcascades/haarcascade_mcs_mouth.xml"
        self.mouth = cv2.CascadeClassifier(self.mouth_fn)

        self.selection = None
        self.drag_start = None
        self.tracking_state = 0
        self.show_backproj = False

        self.face_frame = 0

        cv2.namedWindow('camshift')
        cv2.namedWindow('source')
        #cv2.namedWindow('hist')

        if video_src == "webcam":
            while True:
                ret, img = self.cam.read()
                self.rects = self.faceSearch(img)
                print "Searching for face..."
                if len(self.rects) != 0:
                    break

        else:
            for f in xrange(self.vidFrames):
                img = cv.QueryFrame(self.vidFile)
                tmp = cv.CreateImage(cv.GetSize(img), 8, 3)
                cv.CvtColor(img, tmp, cv.CV_BGR2RGB)
                img = np.asarray(cv.GetMat(tmp))
                print "Searching frame", f+1
                self.face_frame = f
                self.rects = self.faceSearch(img)
                if len(self.rects) != 0:
                    break

    def faceSearch(self, img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        rects = self.detect(gray, self.cascade)

        if len(rects) != 0:
            print "Detected face"
            sizeX = rects[0][2] - rects[0][0]
            sizeY = rects[0][3] - rects[0][1]
            print "Face size is", sizeX, "by", sizeY
            return rects
        else:
            return []

    def detect(self, img, cascade):

        # flags = cv.CV_HAAR_SCALE_IMAGE
        rects = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=2, minSize=(80, 80), flags = cv.CV_HAAR_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        rects[:,2:] += rects[:,:2]
        return rects

    def draw_rects(self, img, rects, color):
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

    def show_hist(self):
        bin_count = self.hist.shape[0]
        bin_w = 24
        img = np.zeros((256, bin_count*bin_w, 3), np.uint8)
        for i in xrange(bin_count):
            h = int(self.hist[i])
            cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        cv2.imshow('hist', img)
        cv.MoveWindow('hist', 0, 440)

    def faceTrack(self, img):
        vis = img.copy()

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

        x0, y0, x1, y1 = self.rects[0]
        self.track_window = (x0, y0, x1-x0, y1-y0)
        hsv_roi = hsv[y0:y1, x0:x1]
        mask_roi = mask[y0:y1, x0:x1]
        hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [16], [0, 180] )
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX);
        self.hist = hist.reshape(-1)
        #self.show_hist()

        vis_roi = vis[y0:y1, x0:x1]
        cv2.bitwise_not(vis_roi, vis_roi)
        vis[mask == 0] = 0

        prob = cv2.calcBackProject([hsv], [0], self.hist, [0, 180], 1)
        prob &= mask
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
        track_box, self.track_window = cv2.CamShift(prob, self.track_window, term_crit)

        if self.show_backproj:
            vis[:] = prob[...,np.newaxis]
        try: cv2.ellipse(vis, track_box, (0, 0, 255), 2)
        except: print track_box

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        xc = track_box[0][0]
        yc = track_box[0][1]

        xsize = track_box[1][0]
        ysize = track_box[1][1]

        x1 = int(xc - (xsize/2))
        y1 = int(yc - (ysize/2))
        x2 = int(xc + (xsize/2))
        y2 = int(yc + (ysize/2))

        roi_rect = y1, y2, x1, x2

        roi = gray[y1:y2, x1:x2]
        vis_roi = img.copy()[y1:y2, x1:x2]

        subrects_left_eye = self.detect(roi.copy(), self.left_eye)
        subrects_mouth = self.detect(roi.copy(), self.mouth)

        if subrects_left_eye != []:
            print "eye:", subrects_left_eye, "in roi:", roi_rect

        self.draw_rects(vis_roi, subrects_left_eye, (255, 0, 0))
        self.draw_rects(vis_roi, subrects_mouth, (0, 255, 0))

        cv2.imshow('test', vis_roi)

        dt = clock() - self.t
        draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        #draw_str(vis, (20, 35), 'frame: %d' % f)

        cv2.imshow('source', img)
        cv.MoveWindow('source', 500, 0)
        cv2.imshow('camshift', vis)


    def run(self):

        if video_src == "webcam":
            while True:
                self.t = clock()
                ret, img = self.cam.read()

                self.faceTrack(img)

                ch = 0xFF & cv2.waitKey(1)
                if ch == 27:
                    break
                if ch == ord('b'):
                    self.show_backproj = not self.show_backproj

        else:
            for f in xrange(self.face_frame, self.vidFrames):
                self.t = clock()
                img = cv.QueryFrame(self.vidFile)
                if type(img) != cv2.cv.iplimage:
                    break

                tmp = cv.CreateImage(cv.GetSize(img), 8, 3)
                cv.CvtColor(img, tmp, cv.CV_BGR2RGB)
                img = np.asarray(cv.GetMat(tmp))

                self.faceTrack(img)

                ch = 0xFF & cv2.waitKey(5)
                if ch == 27:
                    break
                if ch == ord('b'):
                    self.show_backproj = not self.show_backproj

        cv2.destroyAllWindows()


if __name__ == '__main__':
    import sys
    try: video_src = sys.argv[1]
    except: video_src = '1'
    App(video_src).run()

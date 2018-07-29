# USAGE
# python barcode_scanner_video.py

# import the necessary packages
import numpy as np
import cv2
import imutils
import time

from imutils.video import VideoStream
from pyzbar import pyzbar
from face_recog import FaceRecog


class Camera(object):

    def __init__(self):
        # initialize the video stream and allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        self.vs = VideoStream(usePiCamera=False).start()
        self.face_recog = FaceRecog()

    def adjust_gamma(self, image, gamma=0.5):
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    def get_frame(self):

        current_barcode = []
        frame = self.vs.read()
        if frame is None:
            return frame, []

        rgb_frame = imutils.resize(frame, width=500)
        frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)
        # reduce brightness
        frame = self.adjust_gamma(frame)

        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)

        # loop over the detected barcodes
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            current_barcode.append(barcodeData)
            print('barcodedata: {}'.format(barcodeData))

        faces = self.face_recog.process(rgb_frame, draw_on_frame=False)
        for face in faces:
            top, right, bottom, left = face.get('location')
            name = face.get('name')
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes(), current_barcode

    def __del__(self):
        # close the output CSV file do a bit of cleanup
        print("[INFO] cleaning up...")
        cv2.destroyAllWindows()
        # self.vs.stop()
        # self.vs.release()

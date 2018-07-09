# USAGE
# python barcode_scanner_video.py

# import the necessary packages
import numpy as np
import cv2
import imutils
import time

from imutils.video import VideoStream
from pyzbar import pyzbar


class Camera(object):

    def __init__(self):
        # initialize the video stream and allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        self.vs = VideoStream(usePiCamera=False).start()

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

        frame = imutils.resize(frame, width=500)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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

        # cv2.imshow("Scanner", frame)

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes(), current_barcode

    def __del__(self):
        # close the output CSV file do a bit of cleanup
        print("[INFO] cleaning up...")
        cv2.destroyAllWindows()
        # self.vs.stop()
        # self.vs.release()

import configargparse

import cv2 as cv


class Grabber:
    def __init__(self, config):
        self.config = config
        self.vid = None


    def fetch(self):
        return self._fetch_camera()


    def _fetch_camera(self):
        if not self.vid:
            self.vid = cv.VideoCapture(0)


        ret, frame = self.vid.read()
        if not ret:
            return None

        return frame


    def close(self):
        if self.vid:
            self.vid.release()
        

    def _fetch_video(self):
        return None
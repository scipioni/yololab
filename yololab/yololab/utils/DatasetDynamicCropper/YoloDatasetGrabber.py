import os
import cv2 as cv
from PathUtil import changeExt, fixPath
from BoundingBoxes import BoundingBoxes

class YoloDatasetGrabber:
    def get_data(self, img_path):
        img = cv.imread(img_path)
        label_path = changeExt(fixPath(label_path), "txt")
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            bbs = BoundingBoxes(f)
            return img, bbs, label_path

    def write_data(self, img_path, label_path, img, label):
        cv.imwrite(img_path, img)
        with open(label_path , 'w') as f:
            f.write(label)
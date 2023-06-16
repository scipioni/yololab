import os
import cv2 as cv
from .PathUtil import changeExt, fixPath
from .BoundingBoxes import BoundingBoxes

class YoloDatasetGrabber:
    def get_data(self, img_path):
        img = cv.imread(img_path)
        label_path = changeExt(fixPath(img_path), "txt")
        if not os.path.exists(label_path):
            raise Exception(img_path + " doesn't have a label.")
        with open(os.path.join(os.getcwd(), label_path), 'r') as label:
            try: bbs = BoundingBoxes(label)
            except: raise Exception(label_path + " uses an incorrect format.")
            return img, bbs, label_path

    def write_data(self, img_path, label_path, img, label):
        cv.imwrite(img_path, img)
        with open(label_path , 'w') as f:
            f.write(label)
import cv2 as CV
from ultralytics import YOLO
import sys
import time
from yololab.utils.DatasetDynamicCropper.DynamicCropper import DynamicCropper
from yololab.utils.DatasetDynamicCropper.BoundingBoxes import BoundingBoxes
from yololab.utils.DatasetDynamicCropper.YoloDatasetGrabber import YoloDatasetGrabber
from yololab.utils.DatasetDynamicCropper.PathUtil import extractExt
import shutil
import imagesize


import glob

type = '../video_2023-06-16_11-49-59.mp4'

model = YOLO(sys.argv[1])
cap = CV.VideoCapture(type)
frame = 0

try:
    while frame is not None:
        ret, frame = cap.read()
        timestamp = str(int(time.time()))
        results = model(source=frame, show=True, save=False, save_txt=False, save_conf=False, classes=[0], name=f'{timestamp}.txt')
        CV.imwrite(f'{sys.argv[2]}/{timestamp}.jpg', frame)
        width, height = imagesize.get(f'{sys.argv[2]}/{timestamp}.jpg')
        with open(f'{sys.argv[2]}/{int(time.time())}.txt', 'w') as file:
            for result in results:
                for box in result.boxes:
                    for i in range(len(box.cls)):
                        file.write(f"{int(box.cls[i])} {box.xywh[i][0]/width} {box.xywh[i][1]/height} {box.xywh[i][2]/width} {box.xywh[i][3]/height}\n")
except:
    print("Fine estrazione")



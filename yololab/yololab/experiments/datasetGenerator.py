import cv2 as CV
from ultralytics import YOLO
import sys
import time
from yololab.utils.DatasetDynamicCropper.DynamicCropper import DynamicCropper
from yololab.utils.DatasetDynamicCropper.BoundingBoxes import BoundingBoxes
from yololab.utils.DatasetDynamicCropper.YoloDatasetGrabber import YoloDatasetGrabber
from yololab.utils.DatasetDynamicCropper.PathUtil import extractExt
import shutil


import glob

type = '../IMG_6573.mp4'

model = YOLO(sys.argv[1])
cap = CV.VideoCapture(type)
frame = 0 

'''while frame is not None:
    ret, frame = cap.read()
    timestamp = str(int(time.time()))
    results = model(source=frame, show=True, save=False, save_txt=False, save_conf=False, classes=[0], name=f'{timestamp}.txt')
    CV.imwrite(f'{sys.argv[2]}/{timestamp}.jpg', frame)
    with open(f'{sys.argv[2]}/{int(time.time())}.txt', 'w') as file:
        for result in results:
            for box in result.boxes:
                for i in range(len(box.cls)):
                    file.write(f"{int(box.cls[i])} {box.xywh[i][0]} {box.xywh[i][1]} {box.xywh[i][2]} {box.xywh[i][3]}\n")'''

dc = DynamicCropper(640,640)
files = glob.glob(f'{sys.argv[2]}/*.jpg')
yolog = YoloDatasetGrabber()
for file in files:
    try:
        img, bbs, label_path = yolog.get_data(file);
        xM, xm, yM, ym = dc.get_borders(bbs)
        center_x, center_y = dc.get_crop_center(1920, 1080, xM, xm, yM, ym)
        cropped = dc.crop(img, center_x, center_y)
        bbs.to_pixel(1920, 1080)
        bbs.to_cropped(640, 640, xm, ym)
        yolog.write_data(f'{sys.argv[2]}/cropped/{file.split("/")[-1]}', f'{sys.argv[2]}/cropped/{label_path.split("/")[-1]}', cropped, bbs.label())
        #CV.imwrite(f'{sys.argv[2]}/cropped/{file.split("/")[-1]}', cropped)
        
        #shutil.copy(label_path, f'{sys.argv[2]}/cropped/{label_path.split("/")[-1]}')
        print('SIUM')
    except Exception:
        print("FAILATO MALE")

    



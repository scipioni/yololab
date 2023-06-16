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

type = '../../../samples/IMG_6573.mp4'

model = YOLO(sys.argv[1])
cap = CV.VideoCapture(type)
frame = 0 

while frame is not None:
    ret, frame = cap.read()
    timestamp = str(int(time.time()))
    results = model(source=frame, show=True, save=False, save_txt=False, save_conf=False, classes=[0], name=f'{timestamp}.txt')
    CV.imwrite(f'{sys.argv[2]}/{timestamp}.jpg', frame)
    with open(f'{sys.argv[2]}/{int(time.time())}.txt', 'w') as file:
        for result in results:
            for box in result.boxes:
                for i in range(len(box.cls)):
                    file.write(f"{int(box.cls[i])} {box.xywh[i][0]} {box.xywh[i][1]} {box.xywh[i][2]} {box.xywh[i][3]}\n")

def crop_img(img, bbs, img_path):
    cropper = DynamicCropper(640, 640)
    img_w, img_h = imagesize.get(img_path)
    bbs.to_pixel(img_w, img_h)
    xM, xm, yM, ym = cropper.get_borders(bbs)
    borders_exceed = not cropper.check(xM, xm, yM, ym)
    if borders_exceed:
        return False, None, None
    center_x, center_y = cropper.get_crop_center(img_w, img_h, xM, xm, yM, ym)
    cropped_img = cropper.crop(img, center_x, center_y)
    offset_x = center_x - 640 / 2
    offset_y = center_y - 640 / 2
    bbs.to_cropped(640, 640, offset_x, offset_y)
    label = bbs.label()
    return True, cropped_img, label


dc = DynamicCropper(640,640)
files = glob.glob(f'{sys.argv[2]}/*.jpg')
yolog = YoloDatasetGrabber()
for file in files:
    try:
        '''img, bbs, label_path = yolog.get_data(file)
        xM, xm, yM, ym = dc.get_borders(bbs)
        center_x, center_y = dc.get_crop_center(1920, 1080, xM, xm, yM, ym)
        cropped = dc.crop(img, center_x, center_y)
        bbs.to_pixel(1920, 1080)
        bbs.to_cropped(640, 640, xm, ym)
        yolog.write_data(f'{sys.argv[2]}/cropped/{file.split("/")[-1]}', f'{sys.argv[2]}/cropped/{label_path.split("/")[-1]}', cropped, bbs.label())'''
        img, bbs, label_path = yolog.get_data(file)
        val, cropped_img, label = crop_img(img, bbs, file)

        yolog.write_data(f'{sys.argv[2]}/cropped/{file.split("/")[-1]}',
                         f'{sys.argv[2]}/cropped/{label_path.split("/")[-1]}', cropped_img, label)
        #CV.imwrite(f'{sys.argv[2]}/cropped/{file.split("/")[-1]}', cropped)

        #shutil.copy(label_path, f'{sys.argv[2]}/cropped/{label_path.split("/")[-1]}')
        print('SIUM')
    except Exception:
        print("FAILATO MALE")




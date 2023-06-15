import cv2 as CV
from ultralytics import YOLO
import sys
import time

model = YOLO(sys.argv[1])
cap = CV.VideoCapture(0)

while True:
    ret, frame = cap.read()
    timestamp = str(int(time.time()))
    results = model(source=frame, show=True, save=False, save_txt=False, save_conf=False, name=f'{timestamp}.txt')
    CV.imwrite(f'{sys.argv[2]}/{timestamp}.jpg', frame)
    with open(f'{sys.argv[2]}/{int(time.time())}.txt', 'w') as file:
        for result in results:
            for box in result.boxes:
                for i in range(len(box.cls)):
                    file.write(f"{int(box.cls[i])} {box.xywh[i][0]} {box.xywh[i][1]} {box.xywh[i][2]} {box.xywh[i][3]}\n")

from ultralytics import YOLO
import sys

model = YOLO(sys.argv[1])
path = "image.jpg"

results = model.predict(source=0, show=True, save=False, save_txt=True, save_conf=False)
print(results)
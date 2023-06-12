from ultralytics import YOLO

model = YOLO('yolov8n.pt')

model.train(data='C:\\Users\\MarcoLvr.PC-AGNESE\\PycharmProjects\\yololab\\datasets\\fpds\\fpds.yml')
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

model.train(data='C:\\Users\\CJ\\Desktop\\Progetti Git\\Galielo_yololab\\yololab\\datasets\\fpds\\fpds.yml')
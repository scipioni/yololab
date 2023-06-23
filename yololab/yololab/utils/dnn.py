import logging
import os

import cv2 as cv
import numpy as np

try:
    from ultralytics import YOLO
    from ultralytics.yolo.utils.plotting import Annotator
except:
    print("no ultralytics support")



from . import draw
from .body import Body

log = logging.getLogger(__name__)

CLASSES = {0:"up", 1:"down"} # TODO, togliere
colors = np.random.uniform(0, 255, size=(max  (len(CLASSES),80), 3)) # TODO
colors = [(0,255,0), (0,0,255)]

class Net:
    def __init__(self, config):
        self.config = config

    def predict(self, frame):
        self.frame = frame
        self.frame_dirty = None

    def prepare_show(self):
        if self.frame_dirty is None:
            self.frame_dirty = self.frame.copy()

    def show(self, scale=1.0):
        frame = self.frame if self.frame_dirty is None else self.frame_dirty
        if scale != 1.0:
            h, w = frame.shape[:2]
            dim = (int(w * scale), int(h * scale))
            frame = cv.resize(frame, dim, interpolation=cv.INTER_AREA)
        cv.imshow(self.config.model, frame)


class NetOnnx(Net):
    def __init__(self, config):
        super().__init__(config)

        self.model: cv.dnn.Net = cv.dnn.readNetFromONNX(config.model)
        self.model.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        self.model.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
        # self.net = cv.dnn_DetectionModel(self.model)
        # self.net.setInputParams(
        #             size=(640, 640),
        #             mean=(0, 0, 0),
        #             scale=1.0 / 255.0,
        #             swapRB=True,
        #             crop=True,
        #         )

    def predict(self, frame):
        # confThreshold = 0.1
        # nmsThreshold = 0.4

        # classIds, confidences, boxes = self.net.detect(
        #     frame, confThreshold, nmsThreshold
        # )

        # return


        h, w = frame.shape[:2]
        length = max((h, w))
        scale = length/ 640
        image = np.zeros((length, length, 3), np.uint8)
        image[0:h, 0:w] = frame
        blob = cv.dnn.blobFromImage(image, scalefactor=1.0 / 255, size=(640, 640), swapRB=True, crop=True)
        self.model.setInput(blob)
        outputs = self.model.forward()

        self.frame = frame
        self.frame_dirty = None


        # outputs = outputs.transpose((0, 2, 1))

        # class_ids, confs, boxes = list(), list(), list()

        # image_height, image_width, _ = frame.shape
        # x_factor = image_width / 640
        # y_factor = image_height / 640

        # rows = outputs[0].shape[0]

        # for i in range(rows):
        #     row = outputs[0][i]
        #     conf = row[4]
            
        #     classes_score = row[4:]
        #     _,_,_, max_idx = cv.minMaxLoc(classes_score)
        #     class_id = max_idx[1]
        #     if (classes_score[class_id] > .25):
        #         confs.append(conf)
        #         label = CLASSES[int(class_id)]
        #         class_ids.append(label)
                
        #         #extract boxes
        #         x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item() 
        #         left = int((x - 0.5 * w) * x_factor)
        #         top = int((y - 0.5 * h) * y_factor)
        #         width = int(w * x_factor)
        #         height = int(h * y_factor)
        #         box = np.array([left, top, width, height])
        #         boxes.append(box)
                
        # r_class_ids, r_confs, r_boxes = list(), list(), list()

        # indexes = cv.dnn.NMSBoxes(boxes, confs, 0.25, 0.45) 
        # for i in indexes:
        #     r_class_ids.append(class_ids[i])
        #     r_confs.append(confs[i])
        #     r_boxes.append(boxes[i])
        
        # self.prepare_show()
        # for i in indexes:
        #     box = boxes[i]
        #     left = box[0]
        #     top = box[1]
        #     width = box[2]
        #     height = box[3]
            
        #     cv2.rectangle(self.frame_dirty, (left, top), (left + width, top + height), (0,255,0), 3)

        # return

        outputs = np.array([cv.transpose(outputs[0])])
        rows = outputs.shape[1]

        boxes = []
        scores = []
        class_ids = []

        self.prepare_show()

        for i in range(rows):
            classes_scores = outputs[0][i][4:]
            (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv.minMaxLoc(classes_scores)
            if maxScore >= 0.25:
                box = [
                    outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                    outputs[0][i][2], outputs[0][i][3]]
                boxes.append(box)
                scores.append(maxScore)
                class_ids.append(maxClassIndex)

        result_boxes = cv.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)

        self.detections = []
        for i in range(len(result_boxes)):
            index = result_boxes[i]
            box = boxes[index]
            detection = {
                'class_id': class_ids[index],
                'class_name': CLASSES.get(class_ids[index], "noname"),
                'confidence': scores[index],
                'box': box,
                'scale': scale}
            self.detections.append(detection)


            self.draw_bounding_box(self.frame_dirty, class_ids[index], scores[index], round(box[0] * scale), round(box[1] * scale),
                                round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale))

    def show(self, scale=1.0):
        super().show(scale=scale)

    def draw_bounding_box(self, img, class_id, confidence, x, y, x_plus_w, y_plus_h):
        label = f'{CLASSES.get(class_id, "noname")} {confidence:.2f}'
        try:
            color = colors[class_id]
        except:
            color = (255,0,0)
        cv.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

        font = cv.FONT_HERSHEY_SIMPLEX
        text_w, text_h = cv.getTextSize(label, font, 0.5, thickness=2)[0]
        cv.rectangle(img, (x, y-2*text_h), (x+text_w+3, y), color, cv.FILLED)
        cv.putText(img, label, (x+3, y - text_h + 2), font, 0.5, (0,0,0), 1)


class NetYoloPose(Net):
    """
    pytorch-quantization          2.1.2
    torch                         2.0.1
    torchinfo                     1.8.0
    torchmetrics                  0.8.0
    torchvision                   0.15.2

    """

    def __init__(self, config):
        super().__init__(config)

        self.model = YOLO(os.path.join(config.models, f"{config.model}.pt"))
        self.bodies = []

    def predict(self, frame):
        super().predict(frame)
        self.results = self.model.predict(source=frame, stream=False, verbose=False)
        self.bodies = self.calculate_bodies()

    def draw_boxes(self):
        for result in self.results:
            boxes = result.boxes.cpu().numpy()  # get boxes on cpu in numpy
            for box in boxes:  # iterate boxes
                name = result.names[int(box.cls[0])]  # iterate results
                r = box.xyxy[0].astype(int)  # get corner points as int
                cv.rectangle(
                    self.frame_dirty, r[:2], r[2:], (255, 0, 255), 2
                )  # draw boxes on img

    def calculate_bodies(self):
        bodies = []

        keypointsm = self.results[0].keypoints.xy  # squeeze().tolist()
        if len(keypointsm) > 16:
            keypointsm = [keypointsm]

        for keypoints in keypointsm:
            body = Body(i=len(bodies))
            try:
                body.xy_neck = [
                    int((keypoints[5][0] + keypoints[6][0]) / 2),
                    int((keypoints[5][1] + keypoints[6][1]) / 2),
                ]
                body.xy_ilium = [
                    int((keypoints[11][0] + keypoints[12][0]) / 2),
                    int((keypoints[11][1] + keypoints[12][1]) / 2),
                ]
                bodies.append(body)
            except Exception as e:
                log.error(e)

        return bodies

    def draw_keypoints(self):
        keypointsm = self.results[0].keypoints.xy  # squeeze().tolist()
        if len(keypointsm) > 16:
            keypointsm = [keypointsm]

        for keypoints in keypointsm:
            for i, kp in enumerate(keypoints):
                try:
                    x = int(kp[0])
                    y = int(kp[1])
                    confidence = kp[2]
                except:
                    continue
                if confidence > self.config.confidence_min:
                    draw.draw_point(self.frame_dirty, xy=(x, y))
                    draw.draw_text(self.frame_dirty, str(i), (x, y))

    def draw_bodies(self):
        for body in self.bodies:
            body.show(self.frame_dirty)

    def show(self, scale=1.0):
        self.prepare_show()
        if self.config.show_ann:
            self.frame_dirty = self.results[0].plot()
        else:
            self.draw_boxes()
            self.draw_keypoints()
            self.draw_bodies()

        super().show(scale=scale)


""".git/{
    'names': ['person'],
    'boxes': tensor([[x1, y1, x2, y2, conf, cls_idx]]),
    'keypoints': tensor([[x1_kpt_0, y1_kpt_0, score_0], ... [x1_kpt_n, y1_kpt_n, score_n]])
}

Here, the 'boxes' field contains the bounding box coordinates and the confidence score (conf) 
and class index (cls_idx) of the detected object. 
The 'keypoints' field contains the x and y coordinates of the detected keypoints (e.g. left shoulder, right shoulder, etc.) 
and their associated confidence scores. Depending on the specific model architecture used, 
the positions of the keypoints and the order in which they are listed in 'keypoints' may vary.

To extract the location of a specific keypoint (e.g. left shoulder) from the results list, 
you can iterate through the list and check the names of the objects detected in each frame 
(which can be accessed using the 'names' field). Once you have located the object of interest (e.g. a person), 
you can extract the coordinates of the desired keypoint from the 'keypoints' field using indexing. 
However, since the position and ordering of the keypoints may change depending on the specific model architecture used, 
there is no built-in way to get a specific keypoint (like the left shoulder) via a function call.


from ultralytics.yolo.engine.results import Results
from ultralytics.yolo.draw.plotting import Annotator
results: Results = model.predict(frame)[0]

keypoints = results.keypoints.squeeze().tolist()
ann = Annotator(frame)
for i, kp in enumerate(keypoints):
    x = int(kp[0])
    y = int(kp[1])
    ann.text((x, y), str(i))
"""

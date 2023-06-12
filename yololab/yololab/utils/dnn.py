import logging
import os

import cv2 as cv
import numpy as np
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator

from . import draw

log = logging.getLogger(__name__)
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
            h,w = frame.shape[:2]
            dim = (int(w*scale), int(h*scale))
            frame = cv.resize(frame, dim, interpolation = cv.INTER_AREA)
        cv.imshow(self.config.model, frame)


class Body:
    def __init__(self, i):
        self.xy_neck = [0,0]
        self.xy_ilium = [0,0]
        self.i = i

    
    def show(self, frame):
        draw.draw_point(frame, xy=self.xy_neck, color=(255,255,0), radius=8)
        draw.draw_point(frame, xy=self.xy_ilium, color=(255,255,0), radius=8)
        draw.draw_segment(frame, start_point=self.xy_neck, end_point=self.xy_ilium, color=(0,0,255), thickness=3, lineType=8)
        if self.isLaying():
            draw.draw_text(frame, f"laying{self.i}", self.xy_neck, color=(255,0,255))
        else:
            draw.draw_text(frame, f"neck{self.i}", self.xy_neck, color=(255,255,0))

    def isLaying(self):
        return True


    def __repr__(self):
        return f"body i={self.i} neck={self.xy_neck}"
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
            boxes = result.boxes.cpu().numpy()                         # get boxes on cpu in numpy
            for box in boxes:                                          # iterate boxes
                name = result.names[int(box.cls[0])]                                    # iterate results
                r = box.xyxy[0].astype(int)                            # get corner points as int
                cv.rectangle(self.frame_dirty, r[:2], r[2:], (255, 0, 255), 2)   # draw boxes on img


    def calculate_bodies(self):
        bodies = []

        keypointsm = self.results[0].keypoints.xy #squeeze().tolist()
        if len(keypointsm) > 16:
            keypointsm = [keypointsm]

        for keypoints in keypointsm:
            body = Body(i=len(bodies))
            try:
                body.xy_neck = [
                    int((keypoints[5][0] + keypoints[6][0])/2),
                    int((keypoints[5][1] + keypoints[6][1])/2),
                ]
                body.xy_ilium = [
                    int((keypoints[11][0] + keypoints[12][0])/2),
                    int((keypoints[11][1] + keypoints[12][1])/2),
                ]
                bodies.append(body)
            except Exception as e:
                log.error(e)

        return bodies


    def draw_keypoints(self):
        keypointsm = self.results[0].keypoints.xy #squeeze().tolist()
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
                    draw.draw_point(self.frame_dirty, xy=(x,y))
                    draw.draw_text(self.frame_dirty, str(i), (x,y))


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
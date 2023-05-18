import os

import cv2 as cv
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator

from . import utils

class Net:
    def __init__(self, config):
        self.config = config

    def predict(self, frame):
        self.frame = frame
        self.frame_dirty = None

    def prepare_show(self):
        if self.frame_dirty is None:
            self.frame_dirty = self.frame.copy()
    
    def show(self):
        cv.imshow(self.config.model, self.frame if self.frame_dirty is None else self.frame_dirty)


class NetYoloPose(Net):
    def __init__(self, config):
        super().__init__(config)

        self.model = YOLO(os.path.join(config.models, f"{config.model}.pt"))

    def predict(self, frame):
        super().predict(frame)
        self.results = self.model.predict(source=frame, stream=False, verbose=False)
    
    def draw_boxes(self):
        for result in self.results:
            boxes = result.boxes.cpu().numpy()                         # get boxes on cpu in numpy
            for box in boxes:                                          # iterate boxes
                name = result.names[int(box.cls[0])]                                    # iterate results
                r = box.xyxy[0].astype(int)                            # get corner points as int
                cv.rectangle(self.frame_dirty, r[:2], r[2:], (255, 0, 255), 2)   # draw boxes on img

    def draw_keypoints(self):
        for result in self.results:
            keypoints = result.keypoints.squeeze().tolist()
            for i, kp in enumerate(keypoints):
                try:
                    x = int(kp[0])
                    y = int(kp[1])
                except:
                    continue
                utils.draw_point(self.frame_dirty, x=x, y=y)
                utils.draw_text(self.frame_dirty, str(i), x, y)

    def show(self):
        self.prepare_show()
        if self.config.show_ann:
            self.frame_dirty = self.results[0].plot()
        else:
            self.draw_boxes()
            self.draw_keypoints()
        super().show()

  



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
from ultralytics.yolo.utils.plotting import Annotator
results: Results = model.predict(frame)[0]

keypoints = results.keypoints.squeeze().tolist()
ann = Annotator(frame)
for i, kp in enumerate(keypoints):
    x = int(kp[0])
    y = int(kp[1])
    ann.text((x, y), str(i))
"""
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




import logging
import cv2 as cv
import asyncio
import os

import pandas
import numpy

import configargparse

from .timing import timing

from .grabber import DummyGrabber, FileGrabber, WebcamGrabber

from ultralytics import YOLO



log = logging.getLogger(__name__)



class Net:
    def __init__(self, config):
        self.config = config

        self.model = YOLO(os.path.join(config.models, f"{config.model}.pt"))

    def predict(self, frame):
        self.frame = frame
        self.frame_dirty = None
        self.results = self.model.predict(source=frame, stream=False, verbose=False)
    
    def draw_boxes(self):
        if self.frame_dirty is None:
            self.frame_dirty = self.frame.copy()
        for result in self.results:
            boxes = result.boxes.cpu().numpy()                         # get boxes on cpu in numpy
            for box in boxes:                                          # iterate boxes
                name = result.names[int(box.cls[0])]                                    # iterate results
                r = box.xyxy[0].astype(int)                            # get corner points as int
                cv.rectangle(self.frame_dirty, r[:2], r[2:], (255, 0, 255), 2)   # draw boxes on img

    def draw_keypoints(self):
        if self.frame_dirty is None:
            self.frame_dirty = self.frame.copy()
        for result in self.results:
            keypoints = result.keypoints.cpu().numpy()                         # get boxes on cpu in numpy
            for keypoint in keypoints:                                          # iterate boxes
                print(keypoint)

    def show(self):
        if self.config.show_full:
            self.frame_dirty = self.results[0].plot()
        else:
            self.draw_boxes()
            self.draw_keypoints()


        cv.imshow(self.config.model, self.frame if self.frame_dirty is None else self.frame_dirty)


class NetPose(Net):
    pass


async def grab(config):
    if config.dummy:
        grabber = DummyGrabber(config)
    elif config.images:
        grabber = FileGrabber(config, config.images)
    else:
        grabber = WebcamGrabber(config)
    #grabber.grey = net.channels == 1

    net = Net(config)
    
    i = 1
    while True:
        i += 1
        try:
            #with timing("grab"):
            frame, filename = await grabber.get()
        except Exception as e:
            log.error(e)
            continue

        if frame is None:
            break
        h, w = frame.shape[:2]


        net.predict(frame)

        if config.show:
            net.show()

        if grabber.key == "w":
            pass
        #if cv.waitKey(0 if config.step else 1) == ord('q'):
        #    break
  

def main():
    from .config import get_config
    config = get_config()
    loop = asyncio.get_event_loop()


    if config.show_full:
        config.show = True
    loop.run_until_complete(grab(config))
    loop.close()


if __name__ == '__main__':
    main()



# import cv2
# from ultralytics import YOLO

# ip_address = "rtsp://admin:admin123@192.168.1.2:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
# cap = cv2.VideoCapture(ip_address)
# model = YOLO('yolov8n.pt')
# fps = int(cap.get(cv2.CAP_PROP_FPS))

# fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
# frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# show_boxes = False

# out = cv2.VideoWriter('output.mp4', fourcc, fps,(frame_width,frame_height),True )
# while(cap.isOpened()):
#     ret,frame = cap.read()
#     if ret == True:
#         person_found = False
#         results = model(frame, imgsz=640, stream=True, verbose=False)
#         for result in results:
#             for box in result.boxes.cpu().numpy():
#                 if show_boxes:
#                     r = box.xyxy[0].astype(int)
#                     cv2.rectangle(frame, r[:2], r[2:], (255, 255, 255), 2)
#                 cls = int(box.cls[0])
#                 if cls == 0:
#                     person_found = True

#         if person_found:
#             out.write(frame)
        
#         cv2.imshow('Frame', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break

# cap.release()
# out.release()

# cv2.destroyAllWindows()
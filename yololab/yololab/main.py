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



def jls_extract_def():
    
    return 


class Net:
    def __init__(self, config):
        self.config = config

        self.model = YOLO(os.path.join(config.models, f"{config.model}.pt"))

    def predict(self, frame):
        self.frame = frame
        self.frame_dirty = None
        self.results = self.model.predict(source=frame, stream=False, verbose=False)
        # for result in self.results:
        #     boxes = result.boxes  # Boxes object for bbox outputs
        #     print(boxes)
        #     masks = result.masks  # Masks object for segmentation masks outputs
        #     probs = result.probs  # Class probabilities for classification outputs

        # keypoints_data = results[0].keypoints.cpu().numpy()
    
    def draw_boxes(self):
        if self.frame_dirty is None:
            self.frame_dirty = self.frame.copy()
        for result in self.results:
            boxes = result.boxes.cpu().numpy()                         # get boxes on cpu in numpy
            for box in boxes:                                          # iterate boxes
                clss = result.names[int(box.cls[0])]                                    # iterate results
                r = box.xyxy[0].astype(int)                            # get corner points as int
                cv.rectangle(self.frame_dirty, r[:2], r[2:], (255, 0, 255), 2)   # draw boxes on img


    def show(self, boxes=False):
        if boxes:
            self.draw_boxes()
        if self.config.show_full:
            self.frame_dirty = self.results[0].plot()
        #annotated_frame = self.results[0].plot()

        cv.imshow(self.config.model, self.frame if self.frame_dirty is None else self.frame_dirty)


class NetPose(Net):
    pass


# async def inference(frame):

#     # load model
#     # if config.nanodetect:
#     # if config.nanopose:
#     # if config.tinypose:
#     # ecc.
#         model = YOLO('yolov8n-pose.pt')

#     # if config.custom:
#     #     model = YOLO('path/to/desired_model.pt')


#     # predict current frame with the model 
#     # if config.inference:
#         # load frame
#         # im2 = cv.imread(frame)
        
#         # if success:
#             # Run selected model inference on the frame
#         results = model.predict(source=frame, save=False, save_txt=False)
#         # results_data = results()
#         keypoints_data = results[0].keypoints.cpu().numpy()
#         log.debug(keypoints_data)



# 0: 640x512 1 person, 30.6ms
# Speed: 1.7ms preprocess, 30.6ms inference, 4.5ms postprocess per image at shape (1, 3, 640, 640)
# 2023-05-17 10:10:26,789 [INFO] yololab.main tensor([[[2.5525e+02, 2.4555e+02, 9.9452e-01],
#          [2.6997e+02, 2.2429e+02, 9.8994e-01],
#          [2.3725e+02, 2.3267e+02, 9.6483e-01],
#          [3.0796e+02, 2.2982e+02, 9.3911e-01],
#          [2.2942e+02, 2.5026e+02, 5.4499e-01],
#          [3.6097e+02, 3.2694e+02, 9.9497e-01],
#          [2.2534e+02, 3.5869e+02, 9.9249e-01],
#          [3.9520e+02, 4.7004e+02, 9.5639e-01],
#          [2.1457e+02, 5.0807e+02, 9.3612e-01],
#          [4.3145e+02, 5.6790e+02, 8.8335e-01],
#          [2.3889e+02, 4.4709e+02, 8.7891e-01],
#          [3.4676e+02, 5.7993e+02, 8.9241e-01],
#          [2.5619e+02, 5.8888e+02, 8.8156e-01],
#          [3.3986e+02, 6.4000e+02, 5.9961e-02],
#          [2.4307e+02, 6.4000e+02, 5.8399e-02],
#          [3.2277e+02, 6.4000e+02, 2.6976e-03],
#          [2.7015e+02, 6.1640e+02, 2.8066e-03]]], device='cuda:0')











        # Plot the results on the frame
        # annotated_frame = results[0].plot()

        # # Display the annotated frame
        # cv.imshow(" chosen_model + results", annotated_frame)


        # return []


# #getting pose keypoints:
# # 1. inference of the frame
# output = model(frame)
# # 2. extract pose tensor from output
# pose_tensor = output[:, model.model.names.index('pose')]
# # 3. extract key-points from pose tensor (array of size 57, 17 keypoints with x,y coordinates at three scales)
# keypoint_data = pose_tensor[0].cpu().detach().numpy()
# log.info(keypoint_data)


# {
#     'names': ['person'],
#     'boxes': tensor([[x1, y1, x2, y2, conf, cls_idx]]),
#     'keypoints': tensor([[x1_kpt_0, y1_kpt_0, score_0], ... [x1_kpt_n, y1_kpt_n, score_n]])
# }


# async def show_results(results, frame):
#     if len(frame.shape) < 3:  # immagine grey
#         frame_show = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)
#     else:
#         frame_show = frame.copy()
    
#     return frame_show



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


        #results = await inference(frame)

        net.predict(frame)

        if config.show:
            #frame_show = await show_results(results, frame)
            #cv.imshow("image", frame_show)
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
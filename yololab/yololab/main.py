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

from ultralytics.yolo.utils.plotting import Annotator

log = logging.getLogger(__name__)



def jls_extract_def():
    
    return 


class Net:
    def __init__(self, config):
        self.config = config

        self.model = YOLO(os.path.join(config.models, f"{config.model}.pt"))

    def predict(self, frame):
        self.frame = frame
        self.results = self.model.predict(source=frame, save=False, save_txt=False)
        keypoints_data = self.results[0].keypoints.cpu().detach().numpy()


        keypoints_result = self.results[0].keypoints.squeeze().tolist()
        ann = Annotator(frame)
        for i, kp in enumerate(keypoints_result):
            x = int(kp[0])
            y = int(kp[1])
            ann.text((x, y), str(i), txt_color=(0, 0, 255))

        # log.info(keypoints_data)
        log.info(keypoints_result)


    def show(self):
        annotated_frame = self.results[0].plot()

        cv.imshow(self.config.model, annotated_frame)
        # # Display the annotated frame
        # cv.imshow(" chosen_model + results", annotated_frame)


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
    loop.run_until_complete(grab(config))
    loop.close()


if __name__ == '__main__':
    main()

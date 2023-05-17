import logging
import cv2 as cv
import asyncio

import pandas
import numpy

import configargparse

from .timing import timing

from .grabber import DummyGrabber, FileGrabber, WebcamGrabber

from ultralytics import YOLO



log = logging.getLogger(__name__)



def jls_extract_def():
    
    return 


async def inference(frame):

    # load model
    # if config.nanodetect:
    # if config.nanopose:
    # if config.tinypose:
    # ecc.
        model = YOLO('yolov8n-pose.pt')

    # if config.custom:
    #     model = YOLO('path/to/desired_model.pt')


    # predict current frame with the model 
    # if config.inference:
        # load frame
        # im2 = cv.imread(frame)
        
        # if success:
            # Run selected model inference on the frame
        results = model.predict(source=frame, save=False, save_txt=False)
        # results_data = results()
        keypoints_data = results[0].keypoints.cpu().numpy()
        log.debug(keypoints_data)



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
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv.imshow(" chosen_model + results", annotated_frame)


        return []


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


async def show_results(results, frame):
    if len(frame.shape) < 3:  # immagine grey
        frame_show = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)
    else:
        frame_show = frame.copy()
    
    return frame_show



async def grab(config):
    if config.dummy:
        grabber = DummyGrabber(config)
    elif config.images:
        grabber = FileGrabber(config, config.images)
    else:
        grabber = WebcamGrabber(config)
    #grabber.grey = net.channels == 1

    
    
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


        results = await inference(frame)

        if config.show:
            frame_show = await show_results(results, frame)
            cv.imshow("image", frame_show)

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

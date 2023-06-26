# python YOLOv8-TensorRT/infer-det.py --engine models/yolov8n.engine --device cuda:0 --imgs samples/fp1.png


from .yolov8.engine import TRTModule  # isort:skip
import argparse
import asyncio
import logging
import time
from pathlib import Path

import cv2 as cv
#import torch

from .config import CLASSES, COLORS
from .grabber import DummyGrabber, FileGrabber, Grabber, WebcamGrabber, RtspGrabber
# from .yolov8.torch_utils import det_postprocess
# from .yolov8.utils import blob, letterbox, path_to_list

log = logging.getLogger(__name__)

from . import models


#out = cv2.VideoWriter('output.mp4', fourcc, fps,(frame_width,frame_height),True )

async def grab(config, grabber: Grabber, model: models.Model) -> None:
    while True:
        try:
            frame, filename, bboxes = await grabber.get()
        except Exception as e:
            log.error(e)
            raise
            break

        if frame is None:
            break

        if config.filter_class:
            for classId in config.filter_class.split(","):
                if bboxes.has(classId):
                    print("match")

        #print(bboxes)

        #print(config.filter_class)
        model.predict(frame)
        if config.show:
            model.show()


def main():
    from .config import get_config

    config = get_config()

    if config.dummy:
        grabber = DummyGrabber(config)
    elif config.images:
        if "rtsp" in config.images[0]:
            grabber = RtspGrabber(config)
        else:
            grabber = FileGrabber(config, config.images)
    else:
        grabber = WebcamGrabber(config)

    model = models.getModel(config)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(grab(config, grabber, model))
    loop.close()


if __name__ == "__main__":
    main()

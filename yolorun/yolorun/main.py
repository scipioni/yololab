import argparse
import asyncio
import logging
import time
from pathlib import Path

import cv2 as cv

from .config import CLASSES, COLORS
from .grabber import DummyGrabber, FileGrabber, Grabber, WebcamGrabber, RtspGrabber

log = logging.getLogger(__name__)

from . import models


async def grab(config, grabber: Grabber, model: models.Model) -> None:
    while True:
        try:
            frame, filename, bboxes_truth = await grabber.get()
        except Exception as e:
            log.error(e)
            raise
            break

        if frame is None:
            break

        if config.filter_classes_strict:
            for classId in config.filter_classes_strict:
                if bboxes_truth.hasOnly(classId):
                    if config.move:
                        grabber.move(filename, config.move)
        model.predict(frame)

        bboxes_predicted = model.getBBoxes()

        if config.filter_classes:
            if config.merge and config.save:
                bboxes_predicted.merge(bboxes_truth, config.filter_classes).save(frame, filename, config.save)
            else:
                matched = False
                for classId in config.filter_classes:
                    if bboxes_predicted.has(classId):
                        matched = True

                if matched and config.save:
                    bboxes_predicted.save(
                        frame, filename, config.save, include=config.filter_classes
                    )

        if config.show:
            model.prepare_show()
            model.draw_bboxes(bboxes_predicted)
            model.draw_bboxes(bboxes_truth)
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

import asyncio
import logging

import cv2 as cv

from .grabber import DummyGrabber, FileGrabber, WebcamGrabber
from .utils import dnn

log = logging.getLogger(__name__)


async def grab(config, grabber, net):

    while True:
        try:
            frame, filename = await grabber.get()
        except Exception as e:
            log.error(e)
            continue

        if frame is None:
            break

        net.predict(frame)

        if config.show:
            net.show(scale=1)

        if grabber.key == "w":
            pass

        #cv.waitKey(0)
        # if cv.waitKey(0 if config.step else 1) == ord('q'):
        #    break


def main():
    from .config import get_config

    config = get_config()

    if config.show_ann:
        config.show = True

    if "-pose" in config.model:
        net = dnn.NetYoloPose(config)
    else:
        net = dnn.NetOnnx(config)

    if config.dummy:
        grabber = DummyGrabber(config)
    elif config.images:
        grabber = FileGrabber(config, config.images)
    else:
        grabber = WebcamGrabber(config)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(grab(config, grabber, net))
    loop.close()


if __name__ == "__main__":
    main()



import asyncio
import logging

import cv2 as cv

from . import dnn
from .grabber import DummyGrabber, FileGrabber, WebcamGrabber
from .timing import timing

log = logging.getLogger(__name__)




async def grab(config, net):
    if config.dummy:
        grabber = DummyGrabber(config)
    elif config.images:
        grabber = FileGrabber(config, config.images)
    else:
        grabber = WebcamGrabber(config)
    #grabber.grey = net.channels == 1

    
    while True:
        try:
            frame, filename = await grabber.get()
        except Exception as e:
            log.error(e)
            continue

        if frame is None:
            break
        #h, w = frame.shape[:2]

        net.predict(frame)

        if config.show:
            net.show(scale=2)

        if grabber.key == "w":
            pass
        #if cv.waitKey(0 if config.step else 1) == ord('q'):
        #    break
  

def main():
    from .config import get_config
    config = get_config()

    if config.show_ann:
        config.show = True

    net = dnn.NetYoloPose(config)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(grab(config, net))
    loop.close()


if __name__ == '__main__':
    main()


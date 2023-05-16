import logging
import cv2 as cv
import asyncio

from .timing import timing

from .grabber import DummyGrabber, FileGrabber, WebcamGrabber

log = logging.getLogger(__name__)





async def inference(frame):
    pass
    return []


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

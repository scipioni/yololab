import logging
import cv2 as cv

from .grabber import Grabber

log = logging.getLogger(__name__)


def main():
    from .config import get_config
    config = get_config()
    log.info("start")
    

    grabber = Grabber(config)
    
    
    
    while True:
        frame = grabber.fetch()

        if frame is None:
            log.debug("no frame detected, exit")
            grabber.close()
            break


        #####

        #result = model(, frame)



        #####
        
        cv.imshow('frame', frame)
        if cv.waitKey(0 if config.step else 1) == ord('q'):
            break
  
if __name__ == '__main__':
    main()

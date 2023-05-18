

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

    
    i = 1
    while True:
        i += 1
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
            net.show()

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
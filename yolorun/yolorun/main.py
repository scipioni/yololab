# python YOLOv8-TensorRT/infer-det.py --engine models/yolov8n.engine --device cuda:0 --imgs samples/fp1.png


from .yolov8.engine import TRTModule  # isort:skip
import argparse
from pathlib import Path

import cv2
import torch
import time

from .config import CLASSES, COLORS
from .yolov8.torch_utils import det_postprocess
from .yolov8.utils import blob, letterbox, path_to_list
from .grabber import Grabber, DummyGrabber, FileGrabber, WebcamGrabber
import logging
import asyncio

async def grab(config, grabber: Grabber) -> None:
    device = torch.device(config.device)
    engine = TRTModule(config.model, device)
    H, W = engine.inp_info[0].shape[-2:]

    # set desired output names order
    engine.set_desired(['num_dets', 'bboxes', 'scores', 'labels'])
    #bgr = cv2.imread(str(config.imgs))
    
    # i = 0
    # while True:
    #     start_time = time.time() # start time of the loop

    #     draw = bgr.copy()
    #     bgr, ratio, dwdh = letterbox(bgr, (W, H))
    #     rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    #     tensor = blob(rgb, return_seg=False)
    #     dwdh = torch.asarray(dwdh * 2, dtype=torch.float32, device=device)
    #     tensor = torch.asarray(tensor, device=device)
    #     # inference
    #     data = engine(tensor)

    #     bboxes, scores, labels = det_postprocess(data)
    #     bboxes -= dwdh
    #     bboxes /= ratio

    #     for (bbox, score, label) in zip(bboxes, scores, labels):
    #         bbox = bbox.round().int().tolist()
    #         cls_id = int(label)
    #         cls = CLASSES[cls_id]
    #         color = COLORS[cls]
    #         cv2.rectangle(draw, bbox[:2], bbox[2:], color, 2)
    #         cv2.putText(draw,
    #                     f'{cls}:{score:.3f}', (bbox[0], bbox[1] - 2),
    #                     cv2.FONT_HERSHEY_SIMPLEX,
    #                     0.75, [225, 255, 255],
    #                     thickness=2)
    #     i =+ 1
    #     if i % 1 == 0:
    #         print("FPS: ", int(1.0 / (time.time() - start_time))) # FPS = 1 / time to process loop
    #     cv2.imshow('result', draw)
    #     cv2.waitKey(1)
    #     # else:
    #     #     cv2.imwrite(str(save_image), draw)

    while True:
        try:
            frame, filename = await grabber.get()
        except Exception as e:
            log.error(e)
            continue

        if frame is None:
            break
        
        frame, ratio, dwdh = letterbox(frame, (W, H))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        tensor = blob(rgb, return_seg=False)
        dwdh = torch.asarray(dwdh * 2, dtype=torch.float32, device=device)
        tensor = torch.asarray(tensor, device=device)
        # inference
        data = engine(tensor)

        bboxes, scores, labels = det_postprocess(data)
        bboxes -= dwdh
        bboxes /= ratio


        if config.show:
            draw = frame.copy()

        for (bbox, score, label) in zip(bboxes, scores, labels):
            bbox = bbox.round().int().tolist()
            cls_id = int(label)
            cls = CLASSES[cls_id]
            
            if config.show:
                color = COLORS[cls]
                cv2.rectangle(draw, bbox[:2], bbox[2:], color, 2)
                cv2.putText(draw,
                            f'{cls}:{score:.3f}', (bbox[0], bbox[1] - 2),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, [225, 255, 255],
                            thickness=2)

        if config.show:
            cv2.imshow('result', draw)
            cv2.waitKey(1)

# def parse_config() -> argparse.Namespace:
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--engine', default="models/yolov8n.engine", help='engine file')
#     parser.add_argument('--imgs', type=str, help='Images file')
#     parser.add_argument('--show',
#                         action='store_true',
#                         help='Show the detection results')
#     parser.add_argument('--device',
#                         default='cuda:0',
#                         help='TensorRT infer device')
#     config = parser.parse_config()
#     return config


def main():
    from .config import get_config
    config = get_config()

    if config.dummy:
        grabber = DummyGrabber(config)
    elif config.images:
        grabber = FileGrabber(config, config.images)
    else:
        grabber = WebcamGrabber(config)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(grab(config, grabber))
    loop.close()

if __name__ == '__main__':
    main()
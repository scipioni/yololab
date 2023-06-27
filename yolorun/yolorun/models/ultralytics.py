import cv2 as cv
from ultralytics import YOLO

from .__init__ import Model
from yolorun.grabber import BBoxes, BBox


class ModelYolo(Model):
    def __init__(self, config):
        super().__init__(config)

        self.net = YOLO(config.model)
        self.w = 0
        self.h = 0

    def predict(self, frame):
        super().predict(frame)
        self.h, self.w = frame.shape[:2]
        results = self.net(self.frame, verbose=False, stream=True)
        # self.boxes = results[0].boxes
        self.boxes = []
        for result in results:
            for box in result.boxes.cpu().numpy():
                if box.conf[0] > self.config.confidence_min:
                    self.boxes.append(box)

    def getBBoxes(self):
        bboxes = BBoxes()
        for box in self.boxes:
            x1, y1, x2, y2 = box.xyxy[0].astype(int)[:4]
            bboxes.add(
                BBox(
                    box.cls[0],
                    x1,
                    y1,
                    x2,
                    y2,
                    self.w,
                    self.h,
                )
            )
        return bboxes

    def show(self, scale=1.0):
        self.prepare_show()

        for box in self.boxes:
            r = box.xyxy[0].astype(int)
            color = (255, 255, 255)
            cls = int(box.cls[0])
            if cls > 0:
                color = (0, 0, 255)

            confidence = round(box.conf[0] * 100)
            label = f"{cls} {confidence:02}%"
            fsize, _ = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 1.0, 2)
            fw, fh = fsize
            delta = 2

            x1, y1, x2, y2 = r[:4]
            cv.rectangle(self.frame_dirty, r[:2], r[2:], color, 2, lineType=cv.LINE_AA)
            cv.rectangle(
                self.frame_dirty, (x1, y1 - fh - 2 * delta), (x2, y1), color, -1
            )

            cv.putText(
                self.frame_dirty,
                label,
                (r[0], r[1] - delta),
                0,
                0.9,
                (0, 0, 0),
                2,
                lineType=cv.LINE_AA,
            )
        super().show()


# import cv2
# import os
# from ultralytics import YOLO

# # Load the YOLOv8 model
# model = YOLO('abc.pt')

# # Open the video file
# video_path = "path/to/video"
# cap = cv2.VideoCapture(video_path)
# save_path = "dir/to/save"
# # Loop through the video frames
# file_num = 0
# uniques_id=set()
# while cap.isOpened():
#     # Read a frame from the video
#     success, frame = cap.read()

#     if success:
#         # Run YOLOv8 inference on the frame
#         results = model.track(frame, persist=True,conf=0.7)
#         # print(results)
#         if  results[0].boxes.id !=  None:
#             boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)

#             ids = results[0].boxes.id.cpu().numpy().astype(int)
#             for box, id in zip(boxes, ids):
#                 # Check if the id is unique
#                 int_id =int(id)
#                 if  int_id  not  in  unique_id:
#                     unique_id.add(int_id)

#                     # Crop the image using the bounding box coordinates
#                     cropped_img = frame[box[1]:box[3], box[0]:box[2]]

#                     # Save the cropped image with a unique filename
#                     filename = f"cropped_img_{int_id}.jpg"
#                     filepath = os.path.join(save_path, filename)
#                     cv2.imwrite(filepath, cropped_img)

#                 # Draw the bounding box and id on the frame
#                 cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (85, 45, 255), 2, lineType=cv2.LINE_AA)
#                 cv2.putText(
#                     frame,
#                     f"Id {id}",
#                     (box[0], box[1]),
#                     0,
#                     0.9,
#                     [85, 45, 255],
#                     2,
#                     lineType=cv2.LINE_AA
#                 )
#                 cv2.imshow("Detected Frame", frame)
#                 if cv2.waitKey(1) & 0xFF == ord("q"):
#                     break

#         # Break the loop if 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#     else:
#         # Break the loop if the end of the video is reached
#         break

# # Release the video capture object and close the display window
# cap.release()
# cv2.destroyAllWindows()

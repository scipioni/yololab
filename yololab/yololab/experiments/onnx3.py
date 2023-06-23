import cv2 as cv 
import argparse


class ObjectDetector:
    def __init__(self, model_path):
        self.model_path = model_path

        _net = cv.dnn.readNetFromONNX(self.model_path)
        self.model = cv.dnn_DetectionModel(_net)
        self.model.setInputSize(640, 640)
        #self.model.setInputScale(1.0/127.5) # 255 / 2 = 127.5
        #self.model.setInputMean((127.5, 127.5, 127.5)) # mobilenet => [-1, 1]
        self.model.setInputSwapRB(True)

    def detect_object(self, image_path):
        img = cv.imread(image_path)


        classIndex, confidence, bbox = self.model.detect(img, device=0, confThreshold=0.5)



        # # Preprocess image (if needed) and convert to input tensor
        # input_name = self.model.get_inputs()[0].name
        # input_shape = self.model.get_inputs()[0].shape[2:]  # Excluding batch and channel dimensions
        # input_size = tuple(input_shape)
        # resized_image = cv.resize(image, input_size)
        # input_data = np.expand_dims(resized_image.transpose(2, 0, 1), axis=0)

        # # Run inference
        # outputs = self.model.run(None, {input_name: input_data})

        # # Process the output to get bounding box coordinates
        # # Modify this section based on the output structure of your model
        # output = outputs[0]
        # bounding_box = output[0]
        # x, y, w, h = bounding_box

        # # Display the bounding box on the image
        # x, y, w, h = int(x * image.shape[1]), int(y * image.shape[0]), int(w * image.shape[1]), int(h * image.shape[0])
        # cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # # Show the image with the bounding box
        # cv.imshow("Object Detection", image)
        # cv.waitKey(0)
        # cv.destroyAllWindows()        



def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Object Detection using ONNX model')
    parser.add_argument('--model', type=str, help='Path to the ONNX model file')
    parser.add_argument('--image', type=str, help='Path to the image file')
    args = parser.parse_args()

    # Create ObjectDetector instance
    detector = ObjectDetector(args.model)

    # Perform object detection and display the bounding box
    detector.detect_object(args.image)

if __name__ == '__main__':
    main()

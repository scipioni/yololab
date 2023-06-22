import cv2 as cv 
import argparse


class ObjectDetector:
    def __init__(self, model_path):
        self.model_path = model_path

        _net = cv.dnn.readNetFromONNX(self.model_path)
        #net = cv.dnn_DetectionModel(_net)




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

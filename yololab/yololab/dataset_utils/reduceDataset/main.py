import glob
import argparse
from config import *
from dataset_reducer import DatasetReducer
import imagesize

class Reducer:
    def __init__(self, folder_path:str, width:int, heigth:int) -> tuple:
        self.folder_path = folder_path
        self.width = width
        self.height = heigth

    def reduce_dataset(self):
        image_files = glob.glob(self.folder_path + "/*.jpg")
        

        for image_file in image_files:
            converter = DatasetReducer(self.folder_path, self.width, self.height)

            _, _, x_end, y_end = converter.to_wxh(image_file)

            # Convert coordinates
            txt_file = image_file.replace(".jpg", ".txt")
            converter.coordinates_converter(txt_file)

            print(f"Image: {image_file} - Cropped: to ({x_end},{y_end})")

        print("Conversion completed!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset Converter")
    parser.add_argument("--folder", type=str, default=DATASET_FOLDER, help="Path to the dataset folder")
    parser.add_argument("--width", type=int, default=NEW_WIDTH, help="width of new image")
    parser.add_argument("--height", type=int, default=NEW_HEIGHT, help="height of new image")
    args = parser.parse_args()

    dataset_reducer = Reducer(args.folder, args.width, args.height)
    dataset_reducer.reduce_dataset()



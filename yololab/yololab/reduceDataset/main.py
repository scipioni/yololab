import glob
import argparse
from config import DATASET_FOLDER
from dataset_reducer import DatasetConverter

class DatasetConverterManager:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def convert_dataset(self):
        # Find all .jpg files in the folder
        image_files = glob.glob(self.folder_path + "/*.jpg")

        for image_file in image_files:
            converter = DatasetConverter(self.folder_path)

            # Convert image to 640x640
            x_start, y_start, x_end, y_end = converter.to_640x640(image_file)

            # Convert corresponding coordinates
            txt_file = image_file.replace(".jpg", ".txt")
            converter.coordinates_converter(txt_file)

            print(f"Image: {image_file} - Cropped: ({x_start},{y_start}) to ({x_end},{y_end})")

        print("Conversion completed!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset Converter")
    parser.add_argument("--folder", type=str, default=DATASET_FOLDER, help="Path to the dataset folder")
    args = parser.parse_args()

    converter_manager = DatasetConverterManager(args.folder)
    converter_manager.convert_dataset()

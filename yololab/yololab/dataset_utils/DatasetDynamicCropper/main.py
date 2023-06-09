import os, glob
import argparse
import imagesize
import cv2 as cv
from .YoloDatasetGrabber import YoloDatasetGrabber
from .BoundingBoxes import BoundingBoxes
from .DynamicCropper import DynamicCropper

class Main:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(description='Dynamically crops all images in a dataset.')
        parser.add_argument('DIRECTORY', type=str, help='input directory')
        parser.add_argument('-e', '--image-ext', type=str, required=False, help='extension of dataset images - default: .png')
        parser.add_argument('-s', '--size', type=int, required=False, help='cropped image size')
        parser.add_argument('-r', '--recursive', required=False, action='store_true', help='treat input directory as a dataset, recursively processing all subdirectories')
        args = parser.parse_args()

        self.directory_path = args.DIRECTORY
        self.recursive = args.recursive

        if not args.image_ext:
            self.image_extension = ".png"
        else:
            if args.image_ext[0] == ".": self.image_extension = args.image_ext
            else: self.image_extension = "." + args.image_ext
        
        if not args.size: self.cropped_size = 640
        else: self.cropped_size = args.size
        
    def crop_img(self, img, bbs, img_path, label_path):
        img_w, img_h = imagesize.get(img_path)
        cropper = DynamicCropper(img_w, img_h, self.cropped_size, self.cropped_size)
        bbs.to_pixel(img_w, img_h)
        xM, xm, yM, ym = cropper.get_borders(bbs)
        borders_exceed = not cropper.check(xM, xm, yM, ym)
        if borders_exceed:
            return False, None, None
        center_x, center_y = cropper.get_crop_center(img_w, img_h, xM, xm, yM, ym)
        cropped_img = cropper.crop(img, center_x, center_y, img_w, img_h)
        cropped_img_shape = cropped_img.shape
        bbs.to_cropped(cropped_img_shape[1], cropped_img_shape[0], center_x, center_y)
        label = bbs.label()
        return True, cropped_img, label

    def process_file(self, img_path, output_path):
        print(f"\r{img_path}", end="")
        grabber = YoloDatasetGrabber()
        try:
            img, bbs, label_path = grabber.get_data(img_path)
        except:
            print(" has an incorrect label, it wasn't cropped.")
            return False
        processed_file, out_img, out_label = self.crop_img(img, bbs, img_path, label_path)
        if processed_file:
            out_img_path = output_path + "/" + os.path.basename(img_path)
            out_label_path = out_img_path.replace(self.image_extension, ".txt") 
            grabber.write_data(out_img_path, out_label_path, out_img, out_label)
        return processed_file

    def process_directory(self):
        output_path = self.directory_path + "/cropped"
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        # files = glob.glob(self.directory_path + '/*' + self.image_extension)
        # for img_path in files:
        #     grabber = YoloDatasetGrabber()
        #     img, bbs, label_path = grabber.get_data(img_path)
        #     try:
        #                 processed_file = self.process_file(img_path, output_path)
        #         processed_file, out_img, out_label = self.crop_img(img, bbs, img_path, label_path)
        #         if processed_file:
        #             processed_files += 1
        #             out_img_path = output_path + "/" + os.path.basename(img_path)
        #             out_label_path = out_img_path.replace(self.image_extension, ".txt") 
        #             grabber.write_data(out_img_path, out_label_path, out_img, out_label)
        #     except:
        #         print("errorino. IMG: " + img_path)
        processed_files = 0
        for img_path in glob.iglob(self.directory_path + '/*' + self.image_extension):
            processed_file = self.process_file(img_path, output_path)
            if processed_file:
                processed_files += 1
        return processed_files

    def process_directory_recursively(self):
        processed_files = 0
        for root_path, dir_paths, file_paths in os.walk(self.directory_path):
            for img_path in file_paths:
                if img_path.endswith(self.image_extension):
                    img_path = os.path.join(root_path, img_path)
                    directory_path = os.path.dirname(img_path)
                    if not directory_path.replace("\\", "/").endswith("/cropped"):
                        output_path = directory_path + "/cropped"
                        if not os.path.exists(output_path):
                            os.mkdir(output_path)
                        processed_file = self.process_file(img_path, output_path)
                        if processed_file:
                            processed_files += 1
        return processed_files

def main():
    dataset_cropper = Main()
    total_processed_files = 0
    if dataset_cropper.recursive:
        print("Processing dataset...")
        total_processed_files = dataset_cropper.process_directory_recursively()
    else:
        print("Processing directory...")
        total_processed_files = dataset_cropper.process_directory()

    print("\nProcessed {processedCount} files.".format(processedCount = total_processed_files))
    print("All Done!")

if __name__ == '__main__':
    main()

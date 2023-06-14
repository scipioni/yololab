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
        parser = argparse.ArgumentParser(description='Format directory of dataset to yolo format and filter files with laying people in them.')
        parser.add_argument('--sdir', type=str, help='input directory')
        parser.add_argument('-e', '--image-ext', type=str, required=False, help='extension of dataset images - default: .png')
        parser.add_argument('-s', '--size', type=int, required=False, help='cropped image size')
        parser.add_argument('-r', '--recursive', required=False, action='store_true', help='treat input directory as a dataset, recursively processing all subdirectories')
        parser.add_argument('-v', '--verbose', required=False, action='store_true', help='show filenames')
        args = parser.parse_args()

        self.directory_path = args.sdir
        self.recursive = args.recursive
        self.verbose = args.verbose

        if not args.image_ext:
            self.image_extension = ".png"
        else:
            if args.image_ext[0] == ".": self.image_extension = args.image_ext
            else: self.image_extension = "." + args.image_ext
        
        if not args.size: self.cropped_size = 640
        else: self.cropped_size = args.size
        
    def crop_img(self, img, bbs, img_path, label_path):
        cropper = DynamicCropper(self.cropped_size, self.cropped_size)
        img_w, img_h = imagesize.get(img_path)
        bbs.to_pixel(img_w, img_h)
        xM, xm, yM, ym = cropper.get_borders(bbs)
        borders_exceed = not cropper.check(xM, xm, yM, ym)
        if borders_exceed:
            return False, None, None
        center_x, center_y = cropper.get_crop_center(img_w, img_h, xM, xm, yM, ym)
        cropped_img = cropper.crop(img, center_x, center_y)
        offset_x = center_x - self.cropped_size / 2
        offset_y = center_y - self.cropped_size / 2
        bbs.to_cropped(self.cropped_size, self.cropped_size, offset_x, offset_y)
        label = bbs.label()
        return True, cropped_img, label

    def process_directory(self):
        processed_files = 0
        output_path = self.directory_path + "/cropped"
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        files = glob.glob(self.directory_path + '/*' + self.image_extension)
        for img_path in files:
            grabber = YoloDatasetGrabber()
            img, bbs, label_path = grabber.get_data(img_path)
            if self.verbose:
                print(f"\r{img_path}", end="")
            processed_file, out_img, out_label = self.crop_img(img, bbs, img_path, label_path)
            if processed_file:
                processed_files += 1
                out_img_path = output_path + "/" + os.path.basename(img_path)
                out_label_path = out_img_path.replace(self.image_extension, ".txt") 
                grabber.write_data(out_img_path, out_label_path, out_img, out_label)
        return processed_files

    def process_directories_recursively(self, directory_path=None):
        if not directory_path: directory_path = self.directory_path
        processed_files = 0
        for path in glob.glob(directory_path + '/*'):
            if os.path.isdir(path):
                print("Processing {path}...".format(path = path.replace('\\', '/')))
                dir_processed_files = self.process_directories_recursively(path)
                processed_files += dir_processed_files
            elif path.endswith('.txt'):
                processed_file = self.process_file(path)
                if processed_file: processed_files += 1
        return processed_files

def main():
    dataset_cropper = Main()
    total_processed_files = 0
    if dataset_cropper.recursive:
        print("Processing dataset...")
        total_processed_files = dataset_cropper.process_directories_recursively()
    else:
        print("Processing directory...")
        total_processed_files = dataset_cropper.process_directory()

    print("Processed {processedCount} files.".format(processedCount = total_processed_files))
    print("All Done!")

if __name__ == '__main__':
    main()

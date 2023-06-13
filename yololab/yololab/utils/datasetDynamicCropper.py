import os, glob
import argparse
import imagesize
import cv2 as cv
from functools import partial

class DatasetFormatter():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(description='Format directory of dataset to yolo format and filter files with laying people in them.')
        parser.add_argument('DIRECTORY', type=str, help='input directory')
        parser.add_argument('-e', '--image-ext', type=str, required=False, help='extension of dataset images - default: .png')
        parser.add_argument('-r', '--recursive', required=False, action='store_true', help='treat input directory as a dataset, recursively processing all subdirectories')
        args = parser.parse_args()

        self.directory_path = args.DIRECTORY
        self.recursive = args.recursive

        if not args.image_ext:
            self.image_extension = ".png"
        else:
            if args.image_ext[0] == ".": self.image_extension = args.image_ext
            else: self.image_extension = "." + args.image_ext
        
    def convert_list_to_string(self, list, delimiter=""):
        string = ""
        for element in list:
            string += str(element) + delimiter
        string = string[:len(string)-1]
        return string

    def write_to_file(self, filename, lineList):
        with open(filename, 'w') as fp:
            text = self.convert_list_to_string(lineList, "\n")
            fp.write(text)

    def crop_image(self, image, imageWidth, imageHeight, center):
        # middleY, middleX = int(imageHeight / 2), int(imageWidth / 2)
        centerX, centerY = center
        # dimX, dimY = min(640, imageWidth), min(640, imageHeight)
        # cropWidth, cropHeight = int(dimX / 2), int(dimY / 2)
        cropWidth, cropHeight = int(640 / 2), int(640 / 2)
        croppedImage = image[centerY-cropHeight : centerY+cropHeight,
                             centerX-cropWidth : centerX+cropWidth]
        return croppedImage

    def get_crop_center(self, image, imageWidth, imageHeight, marginList):
        middleX, middleY = int(imageWidth / 2), int(imageHeight / 2)
        centerMargines = [middleX + 640 / 2, middleX - 640 / 2,
                          middleY + 640 / 2, middleY - 640 / 2]
        fitsInMiddleMargines = True
        for i in range(4):
            if i % 2 == 0:
                if not centerMargines[i] >= marginList[i]:
                    fitsInMiddleMargines = False
            else:
                if not centerMargines[i] <= marginList[i]:
                    fitsInMiddleMargines = False
        if fitsInMiddleMargines:
            return middleX, middleY
        else:
            centerX = (centerMargines[0]-centerMargines[1]) / 2,
            centerY = (centerMargines[1]-centerMargines[2]) / 2,
            return centerX, centerY
    
    def get_margins(self, boundingBox, marginList):
        xM = boundingBox[1] + boundingBox[3] / 2
        xm = boundingBox[1] - boundingBox[3] / 2
        yM = boundingBox[2] + boundingBox[4] / 2
        ym = boundingBox[2] - boundingBox[4] / 2
        if marginList[0] or xM >= marginList[0]:
            marginList[0] = xM
        if marginList[1] or xm <= marginList[1]:
            marginList[1] = xm
        if marginList[2] or yM >= marginList[2]:
            marginList[2] = yM
        if marginList[3] or ym <= marginList[3]:
            marginList[3] = ym
        return marginList

    def process_file(self, filename):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            try:
                imagename = filename.replace(".txt", self.image_extension)
                imageWidth, imageHeight = imagesize.get(imagename)
                image = cv.imread(imagename)
            except:
                return False

            lineList = []
            marginList = [None, None, None, None]  #xM, xm, yM, ym 
            for line in f:
                boundingBox = line.split()
                for i in range(len(boundingBox)):
                    if i != 0:
                        value = float(boundingBox[i])
                        if value < 0 or value > max(imageWidth, imageHeight):
                            if not self.safe:
                                f.close()
                                os.remove(filename)
                                os.remove(imagename)
                            return False
                        else:
                            boundingBox[i] = value
                marginList = self.get_margins(boundingBox, marginList)

            center = self.get_crop_center(image, imageWidth, imageHeight, marginList)
            croppedImage = self.crop_image(image, imageWidth, imageHeight, center)
            cv.imshow(":[", croppedImage)
            cv.waitKey(0)
        
        return True

    def process_directory(self, directoryPath=None):
        if not directoryPath: directoryPath = self.directory_path
        totalProcessedFiles = 0
        for filename in glob.glob(directoryPath + '/*.txt'):
            processedFile = self.process_file(filename)
            if processedFile: totalProcessedFiles += 1
        return totalProcessedFiles

    def process_directories_recursively(self, directoryPath=None):
        if not directoryPath: directoryPath = self.directory_path
        totalProcessedFiles = 0
        for path in glob.glob(directoryPath + '/*'):
            if os.path.isdir(path):
                print("Processing {path}...".format(path = path.replace('\\', '/')))
                processedFiles = self.process_directories_recursively(path)
                totalProcessedFiles += processedFiles
            elif path.endswith('.txt'):
                processedFile = self.process_file(path)
                if processedFile: totalProcessedFiles += 1
        return totalProcessedFiles

def main():
    formatter = DatasetFormatter()
    totalProcessedFiles = 0
    if formatter.recursive:
        print("Processing dataset...")
        totalProcessedFiles = formatter.process_directories_recursively()
    else:
        print("Processing directory...")
        totalProcessedFiles = formatter.process_directory()

    print("Processed {processedCount} files.".format(processedCount = totalProcessedFiles))
    print("All Done!")

if __name__ == '__main__':
    main()
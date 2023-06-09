import os, glob
import argparse
import imagesize
from functools import partial
import xml.etree.ElementTree as ET

class DatasetFormatter():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--filter', required=False, action='store_true')
        parser.add_argument('--normalize', required=False, action='store_true')
        parser.add_argument('--xml', required=False, action='store_true')
        parser.add_argument('--dir', type=str, required=True)
        parser.add_argument('--threshold', type=str, required=False)
        parser.add_argument('--image-ext', type=str, required=False)
        parser.add_argument('--output-dir', type=str, required=False)
        parser.add_argument('--database', required=False, action='store_true')
        parser.add_argument('--angle-format', required=False, action='store_true')
        parser.add_argument('--verbose', required=False, action='store_true')
        args = parser.parse_args()
        
        self.FILTER = False
        self.NORMALIZE = False
        self.TO_XML = False
        if args.filter:
            self.FILTER = True
            if args.normalize: self.NORMALIZE = True
            if args.xml: self.TO_XML = True
        elif args.normalize:
            self.NORMALIZE = True
            if args.xml: self.TO_XML = True
        elif args.xml:
            self.TO_XML = True
        else: parser.error("At least one of --filter --normalize and --xml required")

        self.DIRECTORY_PATH = args.dir

        if not args.threshold: self.RATIO_THRESHOLD = 2
        elif not args.filter: parser.error("--threshold needs --filter to work")
        else: self.RATIO_THRESHOLD = args.threshold
        
        if not args.image_ext:
            if args.xml: parser.error("--xml needs --image_ext to work")
            else: self.IMAGE_EXTENSION = "jpg"
        elif not args.normalize and not args.xml: parser.error("--image-ext needs --normalize or --xml to work")
        else: self.IMAGE_EXTENSION = args.image_ext

        if not args.angle_format: self.ANGLE_FORMAT = False
        # elif not args.filter and not args.xml: parser.error("--angle-format needs --filter or --xml to work")
        else: self.ANGLE_FORMAT = True

        if args.output_dir: self.OUTPUT_PATH = args.output_dir
        else: self.OUTPUT_PATH = 'formatted_output'

        if args.verbose: self.VERBOSE = True
        else: self.VERBOSE = False

        if args.database:
            self.WORKING_ON_DATABASE = True
            self.create_database_tree()
            self.process_database()
        else:
            self.WORKING_ON_DATABASE = False
            self.create_output_directory()
            print("Processing directory...")
            self.process_directory()
            print("Done!")

    def create_output_directory(self):
        makeDirectory = partial(os.makedirs, exist_ok=True)
        makeDirectory(self.OUTPUT_PATH)

    def create_database_tree(self):
        filteredDirectorylist = ('archive/dataset/person/train-coco', 
                                'archive/dataset/person/test-coco')
        nestedRootPath = partial(os.path.join, self.OUTPUT_PATH)
        makeDirectory = partial(os.makedirs, exist_ok=True)
    
        for pathItems in map(nestedRootPath, filteredDirectorylist):
            makeDirectory(pathItems)

    def convert_list_to_string(self, list, delimiter=""):
        string = ""
        for element in list:
            string += str(element) + delimiter
        string = string[:len(string)-1]
        return string

    def format_to_xml(self, lineList, directoryList, fileBaseName, filePath):
        annotation = ET.Element('annotation')
        folder = ET.SubElement(annotation, 'folder')
        folder.text = directoryList[len(directoryList)-1]
        filename = ET.SubElement(annotation, 'filename')
        filename.text = fileBaseName[:len(fileBaseName)-3] + self.IMAGE_EXTENSION
        path = ET.SubElement(annotation, 'path')
        path.text = filePath[:len(filePath)-3] + self.IMAGE_EXTENSION
        return ET.tostring(annotation)

    def write_to_file(self, filename, lineList, directoryPath=None):
        if not directoryPath: directoryPath = self.DIRECTORY_PATH
        filePath = ""
        fileBaseName = os.path.basename(filename)
        if self.TO_XML:
            fileBaseName = fileBaseName[:len(fileBaseName)-3] + "xml"
            directoryList = []

        if self.WORKING_ON_DATABASE:
            directoryList = directoryPath.split("/")
            directoryList.pop(0)
            formattedDirectory = self.convert_list_to_string(directoryList, "/")
            filePath = self.OUTPUT_PATH + "/" + formattedDirectory + "/" + fileBaseName
        else:
            filePath = self.OUTPUT_PATH + "/" + fileBaseName
        
        if self.TO_XML: 
            with open(filePath, 'wb') as fp:
                text = self.format_to_xml(lineList, directoryList,
                                                    fileBaseName, filePath)
        else:
            with open(filePath, 'w') as fp:
                text = self.convert_list_to_string(lineList, "\n")
                fp.write(text)

    def process_file(self, filename, directoryPath=None):
        if not directoryPath: directoryPath = self.DIRECTORY_PATH
        layingPeopleCount = 0
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            lineList = []
            for line in f:
                numberList = line.split()
                for i in range(len(numberList)):
                    numberList[i] = float(numberList[i])
                
                if self.ANGLE_FORMAT:
                    convertedNumberList = []
                    convertedNumberList.append( numberList[0] )
                    convertedNumberList.append( (numberList[1] + numberList[2]) / 2 )
                    convertedNumberList.append( (numberList[3] + numberList[4]) / 2 )
                    convertedNumberList.append( numberList[2] - numberList[1] )
                    convertedNumberList.append( numberList[4] - numberList[3])
                    numberList = convertedNumberList

                if self.NORMALIZE:
                    imageName = filename[:len(filename)-3] + self.IMAGE_EXTENSION
                    imageWidth, imageHeight = imagesize.get(imageName)
                    numberList[1] = numberList[1] / imageWidth
                    numberList[2] = numberList[2] / imageHeight
                    numberList[3] = numberList[3] / imageWidth
                    numberList[4] = numberList[4] / imageHeight
                
                if self.FILTER:
                    ratio = numberList[3] / numberList[4]
                    if ratio >= self.RATIO_THRESHOLD:
                        numberList[0] = '1'
                        layingPeopleCount += 1
                
                if self.TO_XML: lineList.append(numberList)
                else: lineList.append(self.convert_list_to_string(numberList, " "))
            
            self.write_to_file(filename, lineList, directoryPath)
        if self.VERBOSE and self.FILTER and layingPeopleCount > 0: 
            fileBaseName = os.path.basename(filename)
            if layingPeopleCount == 1: print("{filename} has a laying person".format(filename = fileBaseName))
            else: print("{filename} has {count} laying people".format(filename = fileBaseName,
                                                                      count = layingPeopleCount))
        return layingPeopleCount

    def process_directory(self, directoryPath = None):
        if not directoryPath: directoryPath = self.DIRECTORY_PATH
        totalLayingPeopleCount = 0
        for filename in glob.glob(directoryPath + '/*.txt'):
            fileLayingPeopleCount = self.process_file(filename, directoryPath)
            totalLayingPeopleCount += fileLayingPeopleCount
        if self.FILTER:
            print("{directory} has {count} laying people".format(directory = directoryPath,
                                                                 count = totalLayingPeopleCount))
        return totalLayingPeopleCount

    def process_database(self):
        print("Processing training directory...")
        trainLayingPeopleCount = self.process_directory(self.DIRECTORY_PATH + '/archive/dataset/person/train-coco')
        print("train-coco Done!")

        print("Processing testing directory...")
        testLayingPeopleCount = self.process_directory(self.DIRECTORY_PATH + '/archive/dataset/person/test-coco')
        print("test-coco Done!")

        if self.FILTER:
            print("The database has {count} laying people".format(count = trainLayingPeopleCount + testLayingPeopleCount))
        print("All Done!")

if __name__ == '__main__':
    formatter = DatasetFormatter()
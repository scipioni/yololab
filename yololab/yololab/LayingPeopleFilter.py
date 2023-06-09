import os, glob
import argparse
from functools import partial

class LayingFilter():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--dir', type=str, required=True)
        parser.add_argument('--threshold', type=str, required=False)
        parser.add_argument('--outputDir', type=str, required=False)
        parser.add_argument('--database', required=False, action='store_true')
        parser.add_argument('--printLayingFiles', required=False, action='store_true')
        args = parser.parse_args()

        self.DIRECTORY_PATH = args.dir

        if args.threshold: self.RATIO_THRESHOLD = args.threshold
        else: self.RATIO_THRESHOLD = 2
        
        if args.outputDir: self.OUTPUT_PATH = args.outputDir
        else: self.OUTPUT_PATH = 'filteredDir'

        if args.printLayingFiles: self.PRINT_LAYING_FILES = True
        else: self.PRINT_LAYING_FILES = False

        if args.database:
            self.WORKING_ON_DATABASE = True
            self.filter_database()
        else:
            self.WORKING_ON_DATABASE = False
            self.create_output_directory()
            print("Processing directory...")
            self.filter_directory()
        print("Done!")
    
    def create_output_directory(self):
        makeDirectory = partial(os.makedirs, exist_ok=True)
        makeDirectory(self.OUTPUT_PATH)

    def create_directory_tree(self):
        filteredDirectorylist = ('archive/dataset/person/train-coco', 
                                'archive/dataset/person/test-coco')
        nestedRootPath = partial(os.path.join, self.OUTPUT_PATH)
        makeDirectory = partial(os.makedirs, exist_ok=True)
    
        for pathItems in map(nestedRootPath, filteredDirectorylist):
            makeDirectory(pathItems)

    def create_filtered_file(self, filename, lineList, directoryPath=None):
        if not directoryPath: directoryPath = self.DIRECTORY_PATH
        directoryList = directoryPath.split("/")
        formattedDirectory = ""
        for i in range(len(directoryList)):
            if i > 1 or ( self.WORKING_ON_DATABASE and i > 0 ):
                formattedDirectory += directoryList[i] + "/"
        filePath = ""
        if self.WORKING_ON_DATABASE: filePath = self.OUTPUT_PATH + "/" + formattedDirectory + os.path.basename(filename)
        else: filePath = self.OUTPUT_PATH + "/" + os.path.basename(filename)
        with open(filePath, 'w') as fp:
            full_text = ""
            for line in lineList:
                text = ""
                for element in line:
                    text += element + " "
                text = text[:len(text)-1]
                full_text += text + "\n"
            full_text = full_text[:len(full_text)-1]
            fp.write(full_text)

    def process_file(self, filename, directoryPath=None):
        if not directoryPath: directoryPath = self.DIRECTORY_PATH
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            lineList = []
            for line in f:
                numberList = line.split()
                ratio = float(numberList[3]) / float(numberList[4])
                if ratio >= self.RATIO_THRESHOLD:
                    numberList[0] = '1'
                    if self.PRINT_LAYING_FILENAMES: print(filename, "has a laying person")
                lineList.append(numberList)
            self.create_filtered_file(filename, lineList, directoryPath)

    def filter_directory(self, directoryPath = None):
        if not directoryPath: directoryPath = self.DIRECTORY_PATH
        for filename in glob.glob(directoryPath + '/*.txt'):
            self.process_file(filename, directoryPath)

    def filter_database(self):
        self.create_directory_tree()

        print("Processing train directory...")
        self.filter_directory(self.DIRECTORY_PATH + '/archive/dataset/person/train-coco')
        print("train-coco Done!")

        print("Processing test directory...")
        self.filter_directory(self.DIRECTORY_PATH + '/archive/dataset/person/test-coco')
        print("test-coco Done!")

if __name__ == '__main__':
    filter = LayingFilter()
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
        parser.add_argument('--verbose', required=False, action='store_true')
        args = parser.parse_args()

        self.DIRECTORY_PATH = args.dir

        if args.threshold: self.RATIO_THRESHOLD = args.threshold
        else: self.RATIO_THRESHOLD = 2
        
        if args.outputDir: self.OUTPUT_PATH = args.outputDir
        else: self.OUTPUT_PATH = 'filteredDir'

        if args.verbose: self.VERBOSE = True
        else: self.VERBOSE = False

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

    def convert_list_to_string(self, list, delimiter=""):
        string = ""
        for element in list:
            string += element + delimiter
        string = string[:len(string)-1]
        return string

    def create_filtered_file(self, filename, lineList, directoryPath=None):
        if not directoryPath: directoryPath = self.DIRECTORY_PATH
        filePath = ""
        if self.WORKING_ON_DATABASE:
            directoryList = directoryPath.split("/")
            directoryList.pop(0)
            formattedDirectory = self.convert_list_to_string(directoryList, "/")
            filePath = self.OUTPUT_PATH + "/" + formattedDirectory + "/" + os.path.basename(filename)
        else:
            filePath = self.OUTPUT_PATH + "/" + os.path.basename(filename)
        
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
                ratio = float(numberList[3]) / float(numberList[4])
                if ratio >= self.RATIO_THRESHOLD:
                    numberList[0] = '1'
                    layingPeopleCount += 1
                filteredLine = self.convert_list_to_string(numberList, " ")
                lineList.append(filteredLine)
            self.create_filtered_file(filename, lineList, directoryPath)
        if self.VERBOSE and layingPeopleCount > 0: 
            fileBaseName = os.path.basename(filename)
            if layingPeopleCount == 1: print("{filename} has a laying person".format(filename = fileBaseName))
            else: print("{filename} has {count} laying people".format(filename = fileBaseName,
                                                                      count = layingPeopleCount))
        return layingPeopleCount

    def filter_directory(self, directoryPath = None):
        if not directoryPath: directoryPath = self.DIRECTORY_PATH
        totalLayingPeopleCount = 0
        for filename in glob.glob(directoryPath + '/*.txt'):
            fileLayingPeopleCount = self.process_file(filename, directoryPath)
            totalLayingPeopleCount += fileLayingPeopleCount
        print("{directory} has {count} laying people".format(directory = directoryPath,
                                                             count = totalLayingPeopleCount))
        return totalLayingPeopleCount

    def filter_database(self):
        self.create_directory_tree()

        print("Processing training directory...")
        trainLayingPeopleCount = self.filter_directory(self.DIRECTORY_PATH + '/archive/dataset/person/train-coco')
        print("train-coco Done!")

        print("Processing testing directory...")
        testLayingPeopleCount = self.filter_directory(self.DIRECTORY_PATH + '/archive/dataset/person/test-coco')
        print("test-coco Done!")

        print("The database has {count} laying people".format(count = trainLayingPeopleCount + testLayingPeopleCount))
        print("All Done!")

if __name__ == '__main__':
    filter = LayingFilter()
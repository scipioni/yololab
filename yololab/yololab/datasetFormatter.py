import os, glob
import argparse
import imagesize
from functools import partial
class DatasetFormatter():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--filter', required=False, action='store_true')
        parser.add_argument('--normalize', required=False, action='store_true')
        parser.add_argument('--dir', type=str, required=True)
        parser.add_argument('--threshold', type=str, required=False)
        parser.add_argument('--image-ext', type=str, required=False)
        parser.add_argument('--output-dir', type=str, required=False)
        parser.add_argument('--dataset', required=False, action='store_true')
        parser.add_argument('--angle-format', required=False, action='store_true')
        parser.add_argument('--verbose', required=False, action='store_true')
        args = parser.parse_args()
        
        self.filter = False
        self.normalize = False
        if args.filter:
            self.filter = True
            if args.normalize: self.normalize = True
        elif args.normalize:
            self.normalize = True
        else: parser.error("At least one of --filter and --normalize required")

        self.directory_path = args.dir

        if not args.threshold: self.ratio_threshold = 2
        elif not args.filter: print("Warning: --threshold needs --filter to work", Warning)
        else: self.ratio_threshold = args.threshold
        
        if not args.image_ext:
            self.image_extension = "jpg"
        elif not args.normalize: print("Warning: --image-ext needs --normalize to work")
        else: self.image_extension = args.image_ext

        if not args.angle_format: self.angle_format = False
        else: self.angle_format = True

        if args.output_dir: self.output_path = args.output_dir
        else: self.output_path = 'formatted_output'

        if args.verbose: self.verbose = True
        else: self.verbose = False

        if args.dataset:
            self.working_on_dataset = True
            self.create_dataset_tree()
            self.process_dataset()
        else:
            self.working_on_dataset = False
            self.create_output_directory()
            print("Processing directory...")
            self.process_directory()
            print("Done!")

    def create_output_directory(self):
        makeDirectory = partial(os.makedirs, exist_ok=True)
        makeDirectory(self.output_path)

    def create_dataset_tree(self):
        filteredDirectorylist = ('archive/dataset/person/train-coco', 
                                'archive/dataset/person/test-coco')
        nestedRootPath = partial(os.path.join, self.output_path)
        makeDirectory = partial(os.makedirs, exist_ok=True)
    
        for pathItems in map(nestedRootPath, filteredDirectorylist):
            makeDirectory(pathItems)

    def convert_list_to_string(self, list, delimiter=""):
        string = ""
        for element in list:
            string += str(element) + delimiter
        string = string[:len(string)-1]
        return string

    def write_to_file(self, filename, lineList, directoryPath=None):
        if not directoryPath: directoryPath = self.directory_path
        filePath = ""
        fileBaseName = os.path.basename(filename)

        if self.working_on_dataset:
            directoryList = directoryPath.split("/")
            directoryList.pop(0)
            formattedDirectory = self.convert_list_to_string(directoryList, "/")
            filePath = self.output_path + "/" + formattedDirectory + "/" + fileBaseName
        else:
            filePath = self.output_path + "/" + fileBaseName
        
        with open(filePath, 'w') as fp:
            text = self.convert_list_to_string(lineList, "\n")
            fp.write(text)

    def process_file(self, filename, directoryPath=None):
        if not directoryPath: directoryPath = self.directory_path
        layingPeopleCount = 0
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            lineList = []
            for line in f:
                numberList = line.split()
                for i in range(len(numberList)):
                    if i != 0: numberList[i] = float(numberList[i])
                
                if self.angle_format:
                    convertedNumberList = []
                    convertedNumberList.append( numberList[0] )
                    convertedNumberList.append( (numberList[1] + numberList[2]) / 2 )
                    convertedNumberList.append( (numberList[3] + numberList[4]) / 2 )
                    convertedNumberList.append( numberList[2] - numberList[1] )
                    convertedNumberList.append( numberList[4] - numberList[3])
                    numberList = convertedNumberList

                if self.normalize:
                    imageName = filename[:len(filename)-3] + self.image_extension
                    imageWidth, imageHeight = imagesize.get(imageName)
                    numberList[1] = numberList[1] / imageWidth
                    numberList[2] = numberList[2] / imageHeight
                    numberList[3] = numberList[3] / imageWidth
                    numberList[4] = numberList[4] / imageHeight
                
                if self.filter:
                    ratio = numberList[3] / numberList[4]
                    if ratio >= self.ratio_threshold:
                        numberList[0] = '1'
                        layingPeopleCount += 1
                
                lineList.append(self.convert_list_to_string(numberList, " "))
            
            self.write_to_file(filename, lineList, directoryPath)
        if self.verbose and self.filter and layingPeopleCount > 0: 
            fileBaseName = os.path.basename(filename)
            if layingPeopleCount == 1: print("{filename} has a laying person".format(filename = fileBaseName))
            else: print("{filename} has {count} laying people".format(filename = fileBaseName,
                                                                      count = layingPeopleCount))
        return layingPeopleCount

    def process_directory(self, directoryPath = None):
        if not directoryPath: directoryPath = self.directory_path
        totalLayingPeopleCount = 0
        for filename in glob.glob(directoryPath + '/*.txt'):
            fileLayingPeopleCount = self.process_file(filename, directoryPath)
            totalLayingPeopleCount += fileLayingPeopleCount
        if self.filter:
            print("{directory} has {count} laying people".format(directory = directoryPath,
                                                                 count = totalLayingPeopleCount))
        return totalLayingPeopleCount

    def process_dataset(self):
        

        print("Processing training directory...")
        trainLayingPeopleCount = self.process_directory(self.directory_path + '/archive/dataset/person/train-coco')
        print("train-coco Done!")

        print("Processing testing directory...")
        testLayingPeopleCount = self.process_directory(self.directory_path + '/archive/dataset/person/test-coco')
        print("test-coco Done!")

        if self.filter:
            print("The dataset has {count} laying people".format(count = trainLayingPeopleCount + testLayingPeopleCount))
        print("All Done!")

if __name__ == '__main__':
    formatter = DatasetFormatter()
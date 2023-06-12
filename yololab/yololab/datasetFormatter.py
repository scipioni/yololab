import os, glob
import argparse
import imagesize
from functools import partial

class DatasetFormatter():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(description='Format directory of dataset to yolo format and filter files with laying people in them.')
        parser.add_argument('DIRECTORY', type=str, help='input directory')
        parser.add_argument('-f', '--filter', required=False, action='store_true', help='filter mode')
        parser.add_argument('-n', '--normalize', required=False, action='store_true', help='normalize mode')
        parser.add_argument('-t', '--threshold', type=str, required=False, help='filter width/height ratio threshold - default: 2')
        parser.add_argument('-e', '--image-ext', type=str, required=False, help='extension of dataset images - default: .png')
        parser.add_argument('-r', '--recursive', required=False, action='store_true', help='treat input directory as a dataset, recursively processing all subdirectories')
        parser.add_argument('-a', '--angle-format', required=False, action='store_true', help='use if input txt format uses angles')
        parser.add_argument('-v', '--verbose', required=False, action='store_true', help='show filenames that contain laying people')
        args = parser.parse_args()
        
        self.directory_path = args.DIRECTORY

        self.filter = False
        self.normalize = False
        if args.filter:
            self.filter = True
            if args.normalize: self.normalize = True
        elif args.normalize:
            self.normalize = True
        else: parser.error("At least one of --filter (-f) and --normalize (-n) required")

        if not args.threshold: self.ratio_threshold = 2
        elif not args.filter: print("Warning: --threshold (-t) needs --filter (-f) to work")
        else: self.ratio_threshold = args.threshold
        
        if not args.image_ext:
            self.image_extension = ".png"
        else:
            if args.image_ext[0] == ".": self.image_extension = args.image_ext
            else: self.image_extension = "." + args.image_ext

        if not args.angle_format: self.angle_format = False
        else: self.angle_format = True

        if args.verbose: self.verbose = True
        else: self.verbose = False

        if args.recursive: self.recursive = True
        else: self.recursive = False

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

    def convert_to_yolo(self, numberList):
        convertedNumberList = []
        convertedNumberList.append( numberList[0] )
        convertedNumberList.append( (numberList[1] + numberList[2]) / 2 )
        convertedNumberList.append( (numberList[3] + numberList[4]) / 2 )
        convertedNumberList.append( numberList[2] - numberList[1] )
        convertedNumberList.append( numberList[4] - numberList[3])
        return convertedNumberList
    
    def normalize_values(self, imageWidth, imageHeight, numberList):
        numberList[1] = numberList[1] / imageWidth
        numberList[2] = numberList[2] / imageHeight
        numberList[3] = numberList[3] / imageWidth
        numberList[4] = numberList[4] / imageHeight
        return numberList

    def has_laying_person(self, numberList) -> bool:
        ratio = numberList[3] / numberList[4]
        if ratio >= self.ratio_threshold: return True
        else: return False

    def process_file(self, filename):
        layingPeopleCount = 0
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            try:
                imageName = filename.replace(".txt", self.image_extension)
                imageWidth, imageHeight = imagesize.get(imageName)
            except:
                return False, layingPeopleCount  # return False, 0
            
            lineList = []
            for line in f:
                numberList = line.split()
                for i in range(len(numberList)):
                    if i != 0: numberList[i] = float(numberList[i])
                
                if self.angle_format:
                    numberList = self.convert_to_yolo(numberList)

                if self.normalize:
                    numberList = self.normalize_values(imageWidth, imageHeight, numberList)
                
                if self.filter:
                    if self.has_laying_person(numberList):
                        numberList[0] = '1'
                        layingPeopleCount += 1
                
                lineList.append(self.convert_list_to_string(numberList, " "))
            
            self.write_to_file(filename, lineList)
        
        if self.verbose and self.filter and layingPeopleCount > 0: 
            fileBaseName = os.path.basename(filename)
            if layingPeopleCount == 1: print("{filename} has a laying person".format(filename = fileBaseName))
            else: print("{filename} has {count} laying people".format(filename = fileBaseName,
                                                                      count = layingPeopleCount))
        return True, layingPeopleCount

    def process_directory(self, directoryPath=None):
        if not directoryPath: directoryPath = self.directory_path
        totalProcessedFiles = 0
        totalLayingPeopleCount = 0
        for filename in glob.glob(directoryPath + '/*.txt'):
            processedFile, fileLayingPeopleCount = self.process_file(filename)
            if processedFile: totalProcessedFiles += 1
            totalLayingPeopleCount += fileLayingPeopleCount
        return totalProcessedFiles, totalLayingPeopleCount

    def process_directories_recursively(self, directoryPath=None):
        if not directoryPath: directoryPath = self.directory_path
        totalProcessedFiles = 0
        totalLayingPeopleCount = 0
        for path in glob.glob(directoryPath + '/*'):
            if os.path.isdir(path):
                print("Processing {path}...".format(path = path.replace('\\', '/')))
                processedFiles, layingPeople = self.process_directories_recursively(path)
                totalProcessedFiles += processedFiles
                totalLayingPeopleCount += layingPeople
            elif path.endswith('.txt'):
                processedFile, fileLayingPeopleCount = self.process_file(path)
                if processedFile: totalProcessedFiles += 1
                totalLayingPeopleCount += fileLayingPeopleCount
        if self.filter and directoryPath != self.directory_path:
            print("{path} has {count} laying people.".format(path = directoryPath.replace('\\', '/'),
                                                             count = totalLayingPeopleCount))
        return totalProcessedFiles, totalLayingPeopleCount

def main():
    formatter = DatasetFormatter()
    totalProcessedFiles = 0
    totalLayingPeople = 0
    if formatter.recursive:
        print("Processing dataset...")
        totalProcessedFiles, totalLayingPeople = formatter.process_directories_recursively()
    else:
        print("Processing directory...")
        totalProcessedFiles, totalLayingPeople = formatter.process_directory()

    if formatter.filter:
        print("Found {count} laying people in {path}.".format(count = totalLayingPeople,
                                                              path = formatter.directory_path))
    print("Processed {processedCount} files.".format(processedCount = totalProcessedFiles))
    print("All Done!")

if __name__ == '__main__':
    main()

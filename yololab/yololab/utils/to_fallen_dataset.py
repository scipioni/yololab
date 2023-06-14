import shutil 
import os
import glob
import argparse

class FallenDataset():
    def __init__(self, source_folder:str, destination_folder):
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        else:
            shutil.rmtree(destination_folder)
            os.makedirs(destination_folder)
        self.folder = source_folder
        self.new_folder = destination_folder

    def class_filter(self):
        try:
            for filename in glob.glob(os.path.join(self.folder, '*.txt')):
                with open(filename, 'r') as f:
                    for line in f.readlines():
                        if line[0] == '1':
                            imgfilename = filename.replace(".txt", ".jpg")
                            shutil.copy(os.path.join(self.folder, filename), os.path.join(self.new_folder, filename))
                            shutil.copy(os.path.join(self.folder, imgfilename), os.path.join(self.new_folder, imgfilename))
                        else:
                            continue
                f.close()
        except:
            print("Error reading file " + str(filename))
            
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fallen People Filter")
    parser.add_argument("--src", type=str, default="datasets/prova", help="Path to the source folder")
    parser.add_argument("--dst", type=str, default="datasets/ofpds", help="Path to the destination folder")
    args = parser.parse_args()

    fallen_dataset = FallenDataset(args.src, args.dst)
    fallen_dataset.class_filter()
    

                

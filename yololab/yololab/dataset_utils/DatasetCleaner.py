import os
import argparse
import glob
import shutil

class DatasetCleaner():
    def __init__(self, directory, imgExt) -> None:
        self.directory = directory
        self.imgExt = imgExt

    def checkClass(self):
        path = os.path.join(self.directory, '*txt')
        for file in glob.glob(os.path.join(self.directory, '*txt')):
            with open(file) as f:
                for line in f.readlines():
                    if line[0] == '1' or line[0] == '1.0':

                        self.moveLaying(file)
            f.close()
                    
    def moveLaying(self, path):
        path = path[:-3]
        txtPath = path + 'txt'
        imgPath = path + self.imgExt
        if not os.path.exists('layingDataset'):
            os.mkdir('layingDataset')
        try:
            shutil.copy(txtPath, os.path.join('layingDataset', os.path.basename(txtPath)))
            shutil.copy(imgPath, os.path.join('layingDataset', os.path.basename(imgPath)))
        except:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', default='/home/andrea/Documents/scuola/pcto/yololab/dataset/GOPR1716/images')
    parser.add_argument('--imgExt', default='jpg')
    args = parser.parse_args()
    datasetCleaner = DatasetCleaner(args.dir, args.imgExt)
    datasetCleaner.checkClass()

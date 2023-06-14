import os
import argparse
import glob
import shutil

def main(directory, imgExt):
    def checkClass(directory):
        path = os.path.join(directory, '*txt')
        for file in glob.glob(os.path.join(directory, '*txt')):
            with open(file) as f:
                for line in f.readlines():
                    if line[0] == '1' or line[0] == '1.0':
                        moveLaying(file)
            f.close()
                    
    def moveLaying(path):
        path = path[:-3]
        txtPath = path + 'txt'
        imgPath = path + imgExt
        if not os.path.exists('layingDataset'):
            os.mkdir('layingDataset')
        try:
            shutil.copy(txtPath, os.path.join('layingDataset', os.path.basename(txtPath)))
            shutil.copy(imgPath, os.path.join('layingDataset', os.path.basename(imgPath)))
        except:
            pass

    
    checkClass(directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', default='dataset/GOPR1716/images')
    parser.add_argument('--imgExt', default='jpg')
    args = parser.parse_args()
    main(args.dir, args.imgExt)
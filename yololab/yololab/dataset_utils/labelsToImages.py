import os
import sys
import glob
import shutil
from dsconvert.api.DatasetConverterAPI import DatasetConverterAPI

dc = DatasetConverterAPI()
subfolders= [f.path for f in os.scandir(sys.argv[1]) if f.is_dir()]
for file in subfolders:
    classes = '0\n1'
    with open(f'{file}/images/classes.txt', 'w') as f:
        f.write(classes)
    dc.convert(f'{file}/images', f'{file}/images', 'voc', 'yolo')
    # files = glob.glob(f'{file}/{sys.argv[2]}/*')
    # for label in files:
    #     shutil.move(label, f'{file}/images/{label.split("/")[-1]}')
        


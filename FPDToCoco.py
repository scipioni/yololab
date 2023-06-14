from coco_lib.common import Info, Image, License
from coco_lib.objectdetection import ObjectDetectionDataset, ObjectDetectionAnnotation, ObjectDetectionCategory
import os
from datetime import datetime
import glob

def main():
    # path = os.path.join('test', 'split5')
    # filename = ''
    
    def listSPD(path):
        values = ''
        t = open(path)
        lines = t.readlines()

        for line in lines:
            values = line.strip().split(' ')

        t.close()
        return values
    
    def takesInput(values):
        for i in range(len(values) % 5):
            isLaying = int(values[i])
            xLeft = int(values[i + 1])
            xRight =int(values[i + 2])
            yLeft = int(values[i + 3])
            yRight = int(values[i + 4])
            toCoco(isLaying, xLeft, xRight, yLeft, yRight, path, i)

    def toCoco(isLaying, xLeft, xRight, yLeft, yRight, i):
        bboxW = xRight - xLeft
        bboxH = yRight - yLeft
        print(datetime.now())

        info = Info(
            year = datetime.now().year,
            version = '1.0',
            description = str(isLaying),
            contributor = 'Test',
            url = 'test',
            date_created = datetime.now()
        )

        mit_license = License(
            id = 0,
            name = 'cacca',
            url = 'https/cacca'
        )

        images = [
            Image(
                id = 0,
                width = 640,
                height = 480,
                file_name = path,
                license = mit_license.id,
                flickr_url = '',
                coco_url = '',
                date_captured = datetime.now()
            ),
        ]     

        categories = [
            ObjectDetectionCategory(
                id = 0,
                name = 'image',
                supercategory = ''
            ),
        ]

        annotations = [  # Describe the annotations
            ObjectDetectionAnnotation(
                id=0,
                image_id=0,
                category_id=0,
                segmentation=[],
                area= bboxW * bboxH,
                bbox=[xRight, yRight, xLeft, yLeft],
                iscrowd = 0
            ),
        ]

        dataset = ObjectDetectionDataset(
            info = info,
            images = images,
            licenses = [mit_license],
            categories = categories,
            annotations = annotations
        )

        #os.mkdir('jsonDataset')
        os.chdir('/home/andrea/Documents/scuola/pcto/yololab/jsonDataset')
        jsonFile = 'dataset' + str(i) + '.json'
        jsonFilename = os.path.join('jsonDataset', jsonFile)
        dataset.save(jsonFile, indent=2) 

    # os.chdir('test/split5')
    # files = glob.glob('*.txt')

    for file in glob.glob('test/split5/*.txt'):
        path = file   #os.path.join('test', 'split5', file) 
        #print(file)
        takesInput(listSPD(path))

if __name__ == "__main__":
    main()
'This is a test dataset'




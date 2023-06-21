# ImageID,Source,LabelName,Confidence,XMin,XMax,YMin,YMax,IsOccluded,IsTruncated,IsGroupOf,IsDepiction,IsInside,XClick1X,XClick2X,XClick3X,XClick4X,XClick1Y,XClick2Y,XClick3Y,XClick4Y

# /m/03m3pdh,Sofa bed
# /m/01g317,Person
# /m/03ssj5,Bed

import csv
import imagesize

class OpenimagesGrabber:

    def grab_line(self, line):
        pass

    def grab_img(self, img_id):
        pass

    def grab_label(self, csv):
        pass

    def grab(self, csv_path, img_path):
        with open(csv_path, 'r') as csv:
            reader = csv.DictReader(csvfile)
            for row in reader:

                open_yolo = []

                open_yolo.append(row[LabelName, XMin, XMax, YMin, YMax])

                if row[i]['ImageID'] != row[i+1]['ImageID']:
                    break

                return open_yolo

                yield
    

    def open_norm(self, img_path, open_bbs):

        img_w, img_h = imagesize.get("img_path")

        for line in open_bbs:

            LabelName = open_bbs[0]

            bb_width = open_bbs[2] - open_bbs[1]
            bb_height = open_bbs[4] - open_bbs[3]
            x_center = open_bbs[2] - (bb_width / 2)
            y_center = open_bbs[4] - (bb_height / 2)
            
            if open_bbs[0] == '/m/01g317': # Person class
                LabelName = 0
            if open_bbs[0] == '/m/03ssj5': # Bed class
                LabelName = 1
            if open_bbs[0] == '/m/03m3pdh': # Sofa bed class
                LabelName = 2

            open_bbs[1] = x_center
            open_bbs[2] = y_center
            open_bbs[3] = bb_width
            open_bbs[4] = bb_height
        
        return open_bbs

            

def main():
    grabber = OpenimagesGrabber()
    csv_path = "/run/media/francesco/DATASET/datasets/openimages_v7/open-images-v7/train/labels/detections.csv"
    grabber.grab(csv_path, None)

if __name__ == "__main__":
    main()
import cv2
import imagesize

class DatasetReducer:
    def __init__(self, folder_path:str, width:int, heigth:int) -> tuple:
        self.folder_path = folder_path
        self.width = width
        self.height = heigth

    def to_wxh(self, path:str):
        original_image = cv2.imread(path)

        image_w, image_h = imagesize.get(path)

        x_start = (image_w - self.width) // 2
        x_end = x_start + self.width
        y_start = (image_h - self.height) // 2
        y_end = y_start + self.height

        cropped_image = original_image[y_start:y_end, x_start:x_end]

        cv2.imwrite(path, cropped_image)
        return (x_start, y_start, x_end, y_end)

    def check_bbox(self, line:list, image_w:int, image_h:int):
        return True if (line[1] + line[3]/2 < image_w + self.width/2 and
                        line[1] - line[3]/2 < image_w - self.width/2 and
                        line[2] + line[4]/2 < image_h + self.height/2 and
                        line[2] - line[4]/2 < image_h - self.height/2) else False


    def coordinates_converter(self, filename:str) -> None:
        try:
            with open(filename, "r") as f:
                lines = ""
                image_w, image_h = imagesize.get(filename.replace(".txt", ".jpg")) 
                for line in f.readlines():
                    line = [float(x) for x in line.strip().split()]
                     
                    # new values
                    # print(image_w, image_h)
                    xc  = (line[1] * 640) / image_w
                    yc  = (line[2] * 640) / image_h
                    w = (line[3] * 640) / image_w
                    h = (line[4] * 640) / image_h
                    lines += f"{line[0]} {xc} {yc} {w} {h} \n" if self.check_bbox(line, image_w, image_h) else ""
                
                f.close()

            with open(filename, "w") as f:
                f.write(lines)
        except Exception as e:
            print(f"{e}\nImage skipped")
            pass
        # return lines


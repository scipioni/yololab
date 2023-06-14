import cv2

class DatasetReducer:
    def __init__(self, folder_path:str, width:int, heigth:int) -> tuple:
        self.folder_path = folder_path
        self.width = width
        self.height = heigth

    def to_WxH(self, path:str):
        original_image = cv2.imread(path)

        x_start = (original_image.shape[1] - self.width) // 2
        x_end = x_start + self.width
        y_start = (original_image.shape[0] - self.height) // 2
        y_end = y_start + self.height

        cropped_image = original_image[y_start:y_end, x_start:x_end]

        cv2.imwrite(path, cropped_image)
        return (x_start, y_start, x_end, y_end)

    def coordinates_converter(self, filename:str) -> None:
        try:
            with open(filename, "r") as f:
                flag = True
                lines = ""
                imageW, imageH, _, _ = self.to_WxH(filename.replace(".txt", ".jpg")) 
                for line in f.readlines():
                    line = [float(x) for x in line.strip().split()]
                    # check if the coords are in a 640x640 crop
                    # flag = True if (line[1] + line[3]/2 < imageW and line[2] + line[4] < imageH) else False
                    
                    # new values
                    xc  = (line[1] * 640) / imageW
                    yc  = (line[2] * 640) / imageH
                    w = (line[3] * 640) / imageW
                    h = (line[4] * 640) / imageH
                    lines += f"{line[0]} {xc} {yc} {w} {h} \n" if flag else ""
                
                f.close()

            with open(filename, "w") as f:
                f.write(lines)
        except:
            print("Image skipped")
        # return lines


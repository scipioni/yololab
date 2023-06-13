import cv2

class DatasetConverter:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def to_640x640(self, path):
        original_image = cv2.imread(path)

        x_start = (original_image.shape[1] - 640) // 2
        x_end = x_start + 640
        y_start = (original_image.shape[0] - 640) // 2
        y_end = y_start + 640

        cropped_image = original_image[y_start:y_end, x_start:x_end]

        cv2.imwrite(path, cropped_image)
        return (x_start, y_start, x_end, y_end)

    def coordinates_converter(self, filename):
        try:
            with open(filename, "r") as f:
                flag = True
                lines = ""
                imageW, imageH, _, _ = self.to_640x640(filename.replace(".txt", ".jpg")) 
                for line in f.readlines():
                    line = [float(x) for x in line.strip().split()]
                    # check if the coords are in a 640x640 crop
                    # flag = True if (line[1] + line[3]/2 < imageW and line[2] + line[4] < imageH) else False
                    
                    # new values
                    xc  = (line[1] * 640) / 1920
                    yc  = (line[2] * 640) / 1080
                    w = (line[3] * 640) / 1920
                    h = (line[4] * 640) / 1080
                    lines += f"{line[0]} {xc} {yc} {w} {h} \n" if flag else ""
                
                f.close()

            with open(filename, "w") as f:
                f.write(lines)
        except:
            print("Image skipped")
        # return lines


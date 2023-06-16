import cv2, os, glob, shutil
    
images = []
files = []

def crop(imgFilename):
    img = cv2.imread(imgFilename)

    startRow = (img.shape[0] - 640) // 2
    endRow = startRow + 640
    startCol = (img.shape[1] - 640) // 2
    endCol = startCol + 640
    croppedImg = img[startRow:endRow, startCol:endCol]

    cv2.imwrite(imgFilename, croppedImg)
    return startRow, endRow, startCol, endCol

def bboxControl(startRow, endRow, startCol, endCol, xCenter, yCenter, w, h):
    startRow = startRow / 1920
    endRow = endRow / 1920
    startCol = startCol / 1080
    endCol = endCol / 1080

    xMin = xCenter - w
    xMax = xCenter + w
    yMin = yCenter - h
    yMax = yCenter + h

    if xMin < startRow or xMax > endRow or yMin < startCol or yMax > endCol:
        return False
    
    return True

def dataControl(labelFilename):
    text = ''

    with open(labelFilename) as f:
        for line in f.readlines():
            line = [float(x) for x in line.strip().split(" ")]
            newCoord = coordRecalc(line[1], line[2], line[3], line[4])
            text += f"{line[0]} {newCoord[0]} {newCoord[1]} {newCoord[2]} {newCoord[3]}"
            c = crop(imgFilename)
            print(bboxControl(c[0], c[1], c[2], c[3], line[1], line[2], line[3], line[4]))
            # if not bboxControl(c[0], c[1], c[2], c[3], line[1], line[2], line[3], line[4]):
            #     os.remove(imgFilename)
        f.close()       
    
    writeLabel(text, labelFilename)  
        
def coordRecalc(x, y, w, h):
    newX = (x * 640) / 1080
    newY = (y * 640) / 1920
    newW = (w * 640) / 1080
    newH = (h * 640) / 1920

    return newX, newY, newW, newH

def writeLabel(text, labelFilename):
    with open(labelFilename, "w") as f:
        f.write(text)            
        f.close()

def filenames(dir):
    for img in glob.glob(dir + '/*.jpg'):
        images.append(img)

    for file in glob.glob(dir + '/*.txt'):
        files.append(file)

def deleteTxt(dir='dataset/GOPR1716/images'):
    for file in glob.glob(dir + '/*.txt'):
        os.remove(file)



for i in range(len(images)):
    imgFilename = images[i]
    filename = files[i]
    dataControl(filename)

# deleteTxt()

def main():
    filenames('dataset/GOPR1716/images')
    return 

if __name__ == "__main__":
    main()
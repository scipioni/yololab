from ..data.BoundingBox import BoundingBox


class LabelData:

    def __init__(self, path, imageWidth, imageHeight):
        self.__path = path
        self.__imageWidth = int(imageWidth)
        self.__imageHeight = int(imageHeight)
        self.__objects = []

    def addObject(self, name, minX, minY, maxX, maxY):
        self.__objects.append(BoundingBox(name, minX, minY, maxX, maxY))

    def width(self):
        return self.__imageWidth

    def height(self):
        return self.__imageHeight

    def objects(self):
        return self.__objects

    def path(self):
        return self.__path

    def show(self):
        print(f"Image Path: {self.__path}")
        print(f"Width: {self.__imageWidth}")
        print(f"Height: {self.__imageHeight}")
        print(f"Objects: ")
        for obj in self.__objects:
            obj.print()



class BoundingBox:

    def __init__(self, name, minX, minY, maxX, maxY):
        self.__name = str(name)
        self.__minX = float(minX)
        self.__minY = float(minY)
        self.__maxX = float(maxX)
        self.__maxY = float(maxY)

    def print(self):
        print(f"{self.__name}:")
        print(f"minX: {self.__minX}")
        print(f"minY: {self.__minY}")
        print(f"maxX: {self.__maxX}")
        print(f"maxY: {self.__maxY}")

    def insertion(self, box2):
        xMin = max(self.minX(), box2.minX())
        yMin = max(self.minY(), box2.minY())
        xMax = min(self.maxX(), box2.maxX())
        yMax = min(self.maxY(), box2.maxY())
        if xMin > xMax or yMin > yMax or xMax < xMin or yMax < yMin:
            return 0.0
        width = xMax - xMin
        height = yMax - yMin
        return max(0.0, width * height)

    def name(self):
        return self.__name

    def minX(self):
        return self.__minX

    def minY(self):
        return self.__minY

    def maxX(self):
        return self.__maxX

    def maxY(self):
        return self.__maxY

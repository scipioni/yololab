import imagesize as ImageSize

from ..data.LabelData import LabelData
from ..wrapper.Wrapper import Wrapper
from ..util.PathUtil import findByExtList, changeTargetFile, changeExt


class YOLOWrapper(Wrapper):

    def ext(self):
        return "txt"

    def read(self, path):
        classes = []
        try:
            cpath = changeTargetFile(path, 'classes.txt')
            with open(cpath) as f:
                for line in f.readlines():
                    classes.append(line.replace("\n", ""))
        except:
            raise Exception("Missing classes.txt file")
        width, height = ImageSize.get(findByExtList(path, ['jpg', 'png']))
        self._data = data = LabelData(
            path,
            width,
            height
        )
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                args = line.split(" ")
                args[1] = int(args[1]) * width
                args[3] = int(args[3]) * width
                args[2] = int(args[2]) * height
                args[4] = int(args[4]) * height

                pmin = [int(args[1]) - int(args[3]) / 2, int(args[2]) - int(args[4]) / 2]
                pmax = [int(args[1]) + int(args[3]) / 2, int(args[2]) + int(args[4]) / 2]
                data.addObject(
                    classes[int(args[0])],
                    pmin[0],
                    pmin[1],
                    pmax[0],
                    pmax[1]
                )

    def write(self, path):
        classes = []
        cpath = changeTargetFile(path, 'classes.txt')
        try:
            with open(cpath) as f:
                for line in f.readlines():
                    classes.append(line)
        except:
            raise Exception("Missing classes.txt file")
        with open(changeExt(path, 'txt'), 'w') as f:
            for obj in self._data.objects():
                objClass = None
                for i in range(len(classes)):
                    if obj.name() == classes[i].replace("\n", ""):
                        objClass = i
                        break
                if objClass is None:
                    raise Exception(f"Class not found for element with name: {obj.name()}")
                width = obj.maxX() - obj.minX()
                height = obj.maxY() - obj.minY()
                center = [obj.maxX() - width / 2, obj.maxY() - height / 2]
                f.write(
                    f"{objClass} {center[0] / self._data.width()} {center[1] / self._data.height()} {width / self._data.width()} {height / self._data.height()}\n")

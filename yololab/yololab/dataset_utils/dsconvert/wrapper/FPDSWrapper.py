import imagesize as ImageSize

from ..data.LabelData import LabelData
from ..wrapper.Wrapper import Wrapper
from ..util.PathUtil import findByExtList


class FPDSWrapper(Wrapper):

    def ext(self):
        return "txt"

    def read(self, path):
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
                data.addObject(
                    "laying_person" if int(args[0]) == 1 else "person",
                    args[1],
                    args[3],
                    args[2],
                    args[4]
                )

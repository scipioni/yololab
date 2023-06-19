import base64 as Base64
import json

from ..data.LabelData import LabelData
from ..wrapper.Wrapper import Wrapper
from ..util.PathUtil import changeExt, findByExtList, extractExt


class LabelMeWrapper(Wrapper):

    def ext(self):
        return "json"

    def read(self, path):
        super().read(path)
        f = open(path)
        data = json.load(f)
        self._data = LabelData(
            path,
            data['imageWidth'],
            data['imageHeight']
        )
        for obj in data['shapes']:
            minX = 9999999
            minY = 9999999
            maxX = 0
            maxY = 0
            for point in obj['points']:
                if point[1] < minY:
                    minX = point[0]
                    minY = point[1]
                    continue
                if point[1] > maxY:
                    maxX = point[0]
                    maxY = point[1]
            self._data.addObject(obj['label'], minX, minY, maxX, maxY)

    def write(self, path):
        imgPath = self._data.path()
        imgPath = findByExtList(imgPath, ['jpg', 'png'])
        img = open(imgPath, 'rb')
        data = {
            'version': '4.0.0',
            'flags': {},
            'shapes': [],
            'imagePath': changeExt(self._data.path(), extractExt(imgPath)),
            'imageData': Base64.b64encode(img.read()).decode('utf-8'),
            'imageHeight': self._data.height(),
            'imageWidth': self._data.width()
        }
        for obj in self._data.objects():
            shape = {
                'label': obj.name(),
                'points': [
                    [
                        obj.minX(),
                        obj.minY()
                    ],
                    [
                        obj.minX(),
                        obj.maxY()
                    ],
                    [
                        obj.maxX(),
                        obj.maxY()
                    ],
                    [
                        obj.maxX(),
                        obj.minY()
                    ]
                ],
                'group_id': None,
                'shape_type': 'polygon',
                'flags': {}

            }
            data.get('shapes').append(
                shape
            )
        f = open(changeExt(path, "json"), 'w')
        f.write(json.dumps(data, sort_keys=True, indent=4))

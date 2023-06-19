import datetime
import json

from ..data.LabelData import LabelData
from ..wrapper.Wrapper import Wrapper
from ..util.PathUtil import changeExt, findByExtList, extractExt


class CocoWrapper(Wrapper):

    def ext(self):
        return "json"

    def read(self, path):
        super().read(path)
        f = open(path)
        data = json.load(f)
        self._data = LabelData(
            path,
            data['images'][0]['width'],
            data['images'][0]['height']
        )
        for obj in data['annotations']:
            self._data.addObject(data['categories'][obj['category_id']]['name'], obj['bbox'][0], obj['bbox'][1], obj['bbox'][2], obj['bbox'][3])

    def write(self, path):
        imgPath = self._data.path()
        imgPath = findByExtList(imgPath, ['jpg', 'png'])
        info = {
            'description': 'Dataset converted with DatasetConverter',
            'url': '',
            'version': '1.0',
            'year': int(datetime.datetime.now().year),
            'contributor': 'DatasetConverter',
            'date_created': f'{datetime.datetime.now().year}/{datetime.datetime.now().month}/{datetime.datetime.now().day}'
        }
        licenses = []
        images = [
            {
                'file_name': imgPath.split("/")[-1],
                'height': self._data.height(),
                'width': self._data.width(),
                'id': 1
            }
        ]
        annotations = []
        categories = []
        idx = 0
        for obj in self._data.objects():
            cat = None
            for i in range(len(categories)):
                if categories[i]['name'].replace("\n", "") == obj.name().replace("\n",""):
                    cat = i
                    break
            if cat is None:
                categories.append({
                    'supercategory': obj.name(),
                    'id': len(categories),
                    'name': obj.name()
                })
                cat = len(categories)-1
            annotations.append({
                'segmentation': [],
                'area': (obj.maxX()-obj.minX())*(obj.maxY()-obj.minY()),
                'iscrowd': 0,
                'image_id': 1,
                'bbox': [
                    obj.minX(),
                    obj.minY(),
                    obj.maxX(),
                    obj.maxY()
                ],
                'category_id': cat,
                'id': idx
            })
            idx += 1
        data = {
            'info': info,
            'licenses': licenses,
            'images': images,
            'annotations': annotations,
            'categories': categories

        }
        f = open(changeExt(path, "json"), 'w')
        f.write(json.dumps(data, sort_keys=True, indent=4))

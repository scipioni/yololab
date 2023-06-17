import xml.etree.ElementTree as ET

from ..data.LabelData import LabelData
from ..wrapper.Wrapper import Wrapper


class VOCWrapper(Wrapper):

    def ext(self):
        return "xml"

    def read(self, path):
        xml = ET.parse(path).getroot()
        self._data = LabelData(
            xml.find("path").text,
            xml.find("size").find("width").text,
            xml.find("size").find("height").text,
        )
        for objj in xml.findall("object"):
            obj = objj.find("bndbox")
            self._data.addObject(
                objj.find("name").text,
                obj.find("xmin").text,
                obj.find("ymin").text,
                obj.find("xmax").text,
                obj.find("ymax").text,
            )

    def write(self, path):
        xml = ET.Element('annotation')
        spath = path.split("/")
        self.__xmlAdd(xml, "folder", path.split("/")[len(spath) - 2])
        filename = spath[-1].split(".")
        filename = filename[len(filename) - 2]
        self.__xmlAdd(xml, 'filename', f"{filename}.jpg")
        self.__xmlAdd(xml, 'path', path.replace(spath[-1], f"{filename}.jpg"))
        size = ET.SubElement(xml, 'size')
        self.__xmlAdd(size, 'width', self._data.width())
        self.__xmlAdd(size, 'height', self._data.height())
        self.__xmlAdd(size, 'depth', 3)
        self.__xmlAdd(xml, 'segmented', 0)
        for obj in self._data.objects():
            xmlObj = ET.SubElement(xml, 'object')
            self.__xmlAdd(xmlObj, 'name', obj.name())
            self.__xmlAdd(xmlObj, 'pose', 'Unspecified')
            self.__xmlAdd(xmlObj, 'truncated', 0)
            self.__xmlAdd(xmlObj, 'difficult', 0)
            box = ET.SubElement(xmlObj, 'bndbox')
            self.__xmlAdd(box, 'xmin', int(obj.minX()))
            self.__xmlAdd(box, 'ymin', int(obj.minY()))
            self.__xmlAdd(box, 'xmax', int(obj.maxX()))
            self.__xmlAdd(box, 'ymax', int(obj.maxY()))
        with open(path.replace(spath[-1], f"{filename}.xml"), "wb") as f:
            f.write(ET.tostring(xml))

    def __xmlAdd(self, xml, key, value):
        el = ET.SubElement(xml, key)
        el.text = str(value)

from ..data.LabelData import LabelData


class Wrapper:

    def __init__(self, data=None):
        self._path = None
        self._data = None
        if data is None or data is not LabelData:
            pass
        self._data = data

    def read(self, path):
        self._path = path

    def write(self, path):
        self._path = path

    def data(self):
        return self._data

    def ext(self):
        return None

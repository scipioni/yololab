from ultralytics import YOLO

from .__init__ import Model



class ModelYolo(Model):
    def __init__(self, config):
        super().__init__(config)

        self.net = YOLO(config.model)


    def predict(self, frame):
        super().predict(frame)

        self.results = self.net(self.frame, verbose=False)
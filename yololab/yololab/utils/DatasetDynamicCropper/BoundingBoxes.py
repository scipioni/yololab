class BoundingBoxes:
    def __init__(self, label):
        self.bbs = []
        for line in label:
            bb = line.split()
            for i in range(1, len(bb)):
                bb[i] = float(bb[i])
            bbs.append(bb)
    
    def bb_values(self, i):
        bb = self.bbs[i]
        bb_class = self.bbs[0]
        bb_x = self.bbs[0]
        bb_y = self.bbs[1]
        bb_w = self.bbs[2]
        bb_h = self.bbs[3]
        return bb_class, bb_x, bb_y, bb_w, bb_h

    def label(self):
        label = str(self.bbs[0])
        for i in range(1, len(self.bbs)):
            label += "\n" + str(self.bbs[i])
        return label

    def normalize(self, img_w, img_h):
        pass

    def to_pixel(self, img_w, img_h):
        for i in range(len(self.bbs)):
            bb = self.bbs[i]
            bb[1] = bb[1] * img_w
            bb[2] = bb[2] * img_h
            bb[3] = bb[3] * img_w
            bb[4] = bb[4] * img_h
            self.bbs[i] = bb
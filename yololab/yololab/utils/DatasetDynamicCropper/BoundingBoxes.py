class BoundingBoxes:
    def __init__(self, label, format="normalized"):
        self.format = format
        self.bbs = []
        for line in label:
            bb = line.split()
            for i in range(1, len(bb)):
                if self.is_normalized(): bb[i] = float(bb[i])
                else: bb[i] = int(bb[i])
            bbs.append(bb)
    
    def is_normalized(self):
        format = self.format.str.lower()
        if format == "normalized": return True
        elif format == "pixel": return False
        else:
            txt = "{format} format doesn't exist. Choose between Normalized and Pixel".format(format = format)
            raise Exception(txt)
        return

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
        if self.is_normalized: raise Exception("Bounding boxes are already normalized.")
        self.format = "normalized"
        for i in range(len(self.bbs)):
            bb = self.bbs[i]
            bb[1] = float(bb[1] / img_w)
            bb[2] = float(bb[2] / img_h)
            bb[3] = float(bb[3] / img_w)
            bb[4] = float(bb[4] / img_h)
            self.bbs[i] = bb

    def to_pixel(self, img_w, img_h):
        if not self.is_normalized: raise Exception("Bounding boxes are already in pixel format.")
        self.format = "pixel"
        for i in range(len(self.bbs)):
            bb = self.bbs[i]
            bb[1] = int(bb[1] * img_w)
            bb[2] = int(bb[2] * img_h)
            bb[3] = int(bb[3] * img_w)
            bb[4] = int(bb[4] * img_h)
            self.bbs[i] = bb
    
    def offset(self, offset_x, offset_y):
        if self.is_normalized: raise Exception("Bounding boxes need to be in pixel format.")
        for i in range(len(self.bbs)):
            bb = self.bbs[i]
            bb[1] = bb[1] - int(offset_x)
            bb[2] = bb[2] - int(offset_y)
            self.bbs[i] = bb

    """
    def to_cropped(self, crop_w, crop_h, offset_x, offset_y):
        if self.is_normalized: raise Exception("Bounding boxes need to be in pixel format.")
        self.format = "normalized"
        for i in range(len(self.bbs)):
            bb = self.bbs[i]
            for j in range(1, len(bb)): bb[j] = float(bb[j])
            bb[1] = float((bb[1] - offset_x) / crop_w)
            bb[2] = float((bb[2] - offset_y) / crop_h)
            bb[3] = float(bb[3] / crop_w)
            bb[4] = float(bb[4] / crop_h)
            self.bbs[i] = bb
    """
        
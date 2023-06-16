from .BoundingBoxes import BoundingBoxes

class DynamicCropper:
    def __init__(self, img_w, img_h, crop_w, crop_h):
        self.crop_w = min(img_w, crop_w)
        self.crop_h = min(img_h, crop_h)

    def get_borders(self, bbs):
        bb_class, bb_x, bb_y, bb_w, bb_h = bbs.bb_values(0)
        xM = bb_x + bb_w / 2
        xm = bb_x - bb_w / 2
        yM = bb_y + bb_h / 2
        ym = bb_y - bb_h / 2
        for i in range(1, len(bbs.bbs)):
            bb_class, bb_x, bb_y, bb_w, bb_h = bbs.bb_values(i)
            xM = max(xM, bb_x + bb_w / 2)
            xm = min(xm, bb_x - bb_w / 2)
            yM = max(yM, bb_y + bb_h / 2)
            ym = min(ym, bb_y - bb_h / 2)
        return xM, xm, yM, ym

    def check(self, xM, xm, yM, ym):
        if xM - xm >= int(self.crop_w) or yM - ym >= int(self.crop_h):
            return False
        return True

    def get_crop_center(self, img_w, img_h, xM, xm, yM, ym):
        half_crop_w, half_crop_h = int(self.crop_w / 2), int(self.crop_h / 2)

        # middle_x, middle_y = int(img_w / 2), int(img_h / 2)
        # centerMargines = [middle_x + half_crop_w, middle_x - half_crop_w,
        #                   middle_y + half_crop_h, middle_y - half_crop_h]
        # # fitsInMiddleMargines = True
        # for i in range(4):
        #     if i % 2 == 0:
        #         if not centerMargines[i] >= marginList[i]:
        #             fitsInMiddleMargines = False
        #     else:
        #         if not centerMargines[i] <= marginList[i]:
        #             fitsInMiddleMargines = False
        # if fitsInMiddleMargines:
        #     return middleX, middleY
        # else:

        center_x = int((xM + xm) / 2)
        center_y = int((yM + ym) / 2)

        if half_crop_w <= center_x:
            if center_x > img_w - half_crop_w:
                center_x = img_w - half_crop_w
        else:
            center_x = half_crop_w
        
        if half_crop_h <= center_y:
            if center_y > img_h - half_crop_h:
                center_y = img_h - half_crop_h
        else:
            center_y = half_crop_h
        
        return center_x, center_y

    def crop(self, img, center_x, center_y, img_w, img_h):
        half_crop_w, half_crop_h = int(self.crop_w / 2), int(self.crop_h / 2)
        cropped_img = img[center_y - half_crop_h : center_y + half_crop_h,
                            center_x - half_crop_w : center_x + half_crop_w]
        return cropped_img

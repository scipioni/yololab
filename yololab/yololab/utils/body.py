from . import draw


class Body:
    def __init__(self, i):
        self.xy_neck = [0, 0]
        self.xy_ilium = [0, 0]
        self.i = i

    def show(self, frame):
        draw.draw_point(frame, xy=self.xy_neck, color=(255, 255, 0), radius=8)
        draw.draw_point(frame, xy=self.xy_ilium, color=(255, 255, 0), radius=8)
        draw.draw_segment(
            frame,
            start_point=self.xy_neck,
            end_point=self.xy_ilium,
            color=(0, 0, 255),
            thickness=3,
            lineType=8,
        )
        if self.isLaying():
            draw.draw_text(frame, f"laying{self.i}", self.xy_neck, color=(255, 0, 255))
        else:
            draw.draw_text(frame, f"neck{self.i}", self.xy_neck, color=(255, 255, 0))

    def isLaying(self):
        return True

    def __repr__(self):
        return f"body i={self.i} neck={self.xy_neck}"

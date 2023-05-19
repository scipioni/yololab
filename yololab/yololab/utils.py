import cv2 as cv


def draw_text(image, text="demo", xy=(0,0), fontScale=1, color=(0,255,0)):
    font = cv.FONT_HERSHEY_SIMPLEX
    thickness = 2
    cv.putText(image, text, xy, font, fontScale, color, thickness, cv.LINE_AA)


def draw_point(image, xy=(0,0), radius=5, color=(0, 0, 255)):
    cv.circle(image, xy, radius=radius, color=color, thickness=-1)

def draw_segment(image, start_point=(0,0), end_point=(0,0), color=(0,0,255), thickness=3, lineType=8):
    cv.line(image, start_point, end_point, color=color, thickness=3, lineType=8) 
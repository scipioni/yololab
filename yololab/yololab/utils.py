import cv2 as cv


def draw_text(image, text="demo", x=0, y=0, fontScale=1, color=(0,255,0)):
    font = cv.FONT_HERSHEY_SIMPLEX
    
    thickness = 2
    
    image = cv.putText(image, text, (x,y), font, fontScale, color, thickness, cv.LINE_AA)


def draw_point(image, x=0, y=0, radius=5):
    cv.circle(image, (x,y), radius=radius, color=(0, 0, 255), thickness=-1)

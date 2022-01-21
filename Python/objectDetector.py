import cv2
import approxPolyDP

"""
The following function was used to classify the detected shape. The original 
function could detect other shapes, but the only shapes of interest is a circle and 
a rectangle, which is why no other shapes are checked for.

https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
"""
class ShapeDetector:
    def __init__(self):
        pass
    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        # arc length allows us to get the perimter
        peri = cv2.arcLength(c, True)
        print("Peri in Shape Detector", peri) # Value used in the First principles RDP
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        cs = []
        # if the shape has 4 vertices, it is either a square or a rectangle
        if len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            print("square shape", x,y,w,h)
            ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle" 
        else:
            shape = "circle"
        # return the name of the shape
        return shape
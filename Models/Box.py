import cv2
from numpy import ndarray


class Box:
    def __init__(self, contour: ndarray):
        self.x, self.y, self.w, self.h = cv2.boundingRect(contour)
        self.area = cv2.contourArea(contour)

    def __repr__(self):
        return f"Box(x={self.x}, y={self.y}, w={self.w}, h={self.h})"

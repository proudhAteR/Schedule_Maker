import cv2
from numpy import ndarray

from Models.Tables.Position import Position

class Box:
    def __init__(self, contour: ndarray):
        self.x, self.y, self.w, self.h = cv2.boundingRect(contour)
        self.pos = self.__get_position()
        self.area = cv2.contourArea(contour)

    def __repr__(self):
        return f"Box(x={self.x}, y={self.y}, w={self.w}, h={self.h})"

    def __get_position(self) -> Position:
        return Position(self.x + self.w, self.y + self.h)

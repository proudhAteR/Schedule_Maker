import os

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from numpy import ndarray

from Models.Box import Box
from Utils.FileHandler import FileHandler


class ImageHandler(FileHandler):

    def __init__(self):
        self.contrast_factor = 1.5
        self.sharpen_factor = 120

    def enhance_image_for_ocr(self, img: Image, max_side_limit: int = 4000) -> tuple[Image, list]:
        rgb_img = img.convert('RGB')
        np_img = np.array(rgb_img)
        np_img = self.__deskew_image(np_img)
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), self.contrast_factor)
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        # Get text and table layers
        text_image = np.array(Image.fromarray(thresh))
        table_mask = self.__table_mask(text_image)

        overlay = cv2.addWeighted(text_image, 1.0, table_mask, 0.6, 0)
        if len(overlay.shape) == 2:
            overlay = cv2.cvtColor(overlay, cv2.COLOR_GRAY2BGR)

        boxes = self.__contour(table_mask, overlay)

        gray = Image.fromarray(overlay)
        contrast = ImageEnhance.Contrast(gray).enhance(self.contrast_factor)
        sharpened = contrast.filter(ImageFilter.UnsharpMask(radius=0.75, percent=self.sharpen_factor, threshold=3))

        width, height = sharpened.size
        scale = min(max_side_limit / width, max_side_limit / height, 2)  # Avoid enlarging beyond 2x

        new_size = (int(width * scale), int(height * scale))
        res = sharpened.resize(new_size, resample=Image.Resampling.LANCZOS)

        return res.convert('RGB'), boxes

    @classmethod
    def __deskew_image(cls, img: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        angle = 0
        if lines is not None:
            for rho, theta in lines[0]:
                angle = (theta * 180 / np.pi) - 90
                if abs(angle) < 45:
                    break
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    @classmethod
    def get_processed_filename(cls, original_path: str) -> str:
        base, ext = os.path.splitext(original_path)
        return f"{base}_processed.jpg"

    @classmethod
    def get_image_dpi(cls, img: Image) -> int:
        return img.info.get('dpi', (300, 300))[0] if 'dpi' in img.info else 300

    @classmethod
    def get_image(cls, path: str) -> Image:

        if cls._is_pdf(path):
            return cls.convert_pdf_to_image(path)

        return Image.open(path)

    @classmethod
    def paddle_conversion(cls, image: Image) -> ndarray:
        return np.array(image)

    @classmethod
    def __table_mask(cls, array: ndarray) -> ndarray:
        # Invert for line detection
        binary = cv2.bitwise_not(array)

        # Clean small dots (text noise)
        kernel = np.ones((2, 2), np.uint8)
        opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

        # Combine horizontal and vertical masks
        h_mask = cls.__h_mask(opened)
        v_mask = cls.__v_mask(opened)

        return cv2.add(h_mask, v_mask)

    @classmethod
    def __h_mask(cls, array: ndarray) -> ndarray:
        cols = array.shape[1]
        horizontal_size = max(10, cols // 20)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
        eroded = cv2.erode(array, kernel, iterations=1)
        return cv2.dilate(eroded, kernel, iterations=1)

    @classmethod
    def __v_mask(cls, array: ndarray) -> ndarray:
        rows = array.shape[0]
        vertical_size = max(10, rows // 20)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))
        eroded = cv2.erode(array, kernel, iterations=1)
        return cv2.dilate(eroded, kernel, iterations=1)

    @classmethod
    def __contour(cls, mask: ndarray, image: ndarray) -> list[Box]:
        boxes = []
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            box = Box(cnt)
            boxes.append(box)

            aspect_ratio = box.w / box.h if box.h != 0 else 0

            if box.area > 500 and box.w > 40 and box.h > 25 and 0.2 < aspect_ratio < 6.0:
                cls.__draw_contour(box, image)

        return boxes

    @classmethod
    def __draw_contour(cls, box: Box, image: ndarray):
        cv2.rectangle(image, (box.x, box.y), (box.x + box.w, box.y + box.h), (0, 255, 0), 2)

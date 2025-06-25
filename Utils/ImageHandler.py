import os

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

from Utils.FileHandler import FileHandler


class ImageHandler:

    def __init__(self):
        self.contrast_factor = 1.5
        self.sharpen_factor = 120

    def enhance_image_for_ocr(self, img: Image) -> Image:
        rgb_img = img.convert("RGB")
        np_img = np.array(rgb_img)
        np_img = self.__deskew_image(np_img)
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), self.contrast_factor)
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        gray = Image.fromarray(thresh)
        np_img = np.array(gray)
        np_img = self.__add_border(np_img)
        gray = Image.fromarray(np_img)
        contrast = ImageEnhance.Contrast(gray).enhance(self.contrast_factor)
        sharpened = contrast.filter(ImageFilter.UnsharpMask(radius=0.75, percent=self.sharpen_factor, threshold=2))
        return sharpened.resize((sharpened.width * 2, sharpened.height * 2), resample=Image.Resampling.LANCZOS)

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
        return f"{base}_processed{ext}"

    @classmethod
    def get_image_dpi(cls, img: Image) -> int:
        return img.info.get('dpi', (300, 300))[0] if 'dpi' in img.info else 300

    @classmethod
    def __add_border(cls, img: np.ndarray) -> np.ndarray:
        return cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    @classmethod
    def get_image(cls, path: str) -> Image:

        if FileHandler.is_pdf(path):
            return FileHandler.convert_pdf_to_image(path)

        return Image.open(path)

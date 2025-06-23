import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
import logging
import cv2
import numpy as np
import re
from Services.FileService import FileService

logger = logging.getLogger()


def _get_processed_filename(original_path: str) -> str:
    base, ext = os.path.splitext(original_path)
    return f"{base}_processed{ext}"


def get_image_dpi(img: Image) -> int:
    return img.info.get('dpi', (300, 300))[0] if 'dpi' in img.info else 300


class TesseractService:
    def __init__(self,
                 config: str = r'--psm 11 --oem 1 --dpi {dpi}', lang: str = 'fra+eng', debug: bool = False,
                 contrast_factor: float = 1.5, sharpen_factor: int = 120):
        self.config = config
        self.lang = lang
        self.debug = debug
        self.contrast_factor = contrast_factor
        self.sharpen_factor = sharpen_factor

        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise RuntimeError(f"Tesseract not found: {e}")

    def extract(self, path: str, custom_config: str = None) -> tuple[str, int]:
        path = 'schedules/' + path
        if not FileService.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")

        if FileService.is_pdf(path):
            original_image = FileService.convert_pdf_to_images(path)
        else:
            original_image = Image.open(path)

        try:
            if self.debug:
                logger.info(f"Image size: {original_image.size}, mode: {original_image.mode}")

            enhanced_image = self.__enhance_image_for_ocr(original_image)

            config = custom_config if custom_config else self.config.format(dpi=get_image_dpi(original_image))
            data = pytesseract.image_to_data(enhanced_image, lang=self.lang, config=config,
                                             output_type=pytesseract.Output.DICT)

            # Filter text with confidence > 50
            text_parts = [d for i, d in enumerate(data['text']) if float(data['conf'][i]) > 50 if data['conf'][i]]
            text = ' '.join(text_parts) if text_parts else ''

            # Calculate average confidence
            conf_scores = [float(c) for c in data['conf'] if c and float(c) > 50]
            avg_conf = sum(conf_scores) / len(conf_scores) if conf_scores else 0.0

            if self.debug:
                processed_path = _get_processed_filename(path)
                enhanced_image.save(processed_path)
                logger.info(f"Saved processed image to: {processed_path}")
                logger.info(f"Extracted {len(text)} characters with config: {config}, avg conf: {avg_conf}")

            return text.strip(), int(avg_conf)
        except Exception as e:
            logger.error(f"OCR failed for {path}: {e}")
            raise

    def __enhance_image_for_ocr(self, img: Image) -> Image:
        rgb_img = img.convert("RGB")
        np_img = np.array(rgb_img)
        np_img = self.__deskew_image(np_img)
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 1.5)
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
    def __add_border(cls, img: np.ndarray) -> np.ndarray:
        return cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])

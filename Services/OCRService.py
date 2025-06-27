from PIL import Image

from Interfaces.OCR import OCR
from Utils.FileHandler import FileHandler
from Utils.ImageHandler import ImageHandler
from Utils.Logger import Logger


class OCRService:

    def __init__(self, ocr: OCR, lang: str = None, config: str = None, debug: bool = False):
        self.ocr: OCR = ocr.init(lang, debug=debug, config=config)
        self.debug = debug
        self.image = ImageHandler()

    def extract(self, image_path: str, conf_min: int = 50):
        image_path = FileHandler.in_schedules(image_path)

        if not FileHandler.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        enhanced = self.__process(
            ImageHandler.get_image(image_path)
        )

        try:

            res = self.ocr.extract(enhanced, conf_min)

            if self.debug:
                processed_path = ImageHandler.get_processed_filename(image_path)
                enhanced.save(processed_path)
                Logger.info(f"Saved processed image to: {processed_path}")
                Logger.info(f"Extracted {len(res)} characters")

            return res
        except Exception:
            raise

    def __process(self, img: Image) -> Image:
        return self.image.enhance_image_for_ocr(img)

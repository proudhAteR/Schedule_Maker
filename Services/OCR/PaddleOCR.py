import json

from PIL import Image

from paddleocr import PaddleOCR
from paddlex.inference.pipelines.ocr.result import OCRResult

from Interfaces.OCR import OCR
from Utils.ImageHandler import ImageHandler
from Utils.Logger import Logger


class C_PaddleOCR(OCR):
    def __init__(self):
        super().__init__()
        self.ocr = None

    def init(self, lang: str = None, debug: bool = False, config: str = None) -> "C_PaddleOCR":
        lang = lang or 'fra'
        self.lang = 'fr' if 'fra' in lang else 'en'
        self.debug = debug

        try:
            self.config = json.loads(config) if config else {}
        except json.JSONDecodeError as e:
            Logger.error(f"Invalid config format: {e}")
            self.config = {}

        try:
            self.ocr: PaddleOCR = PaddleOCR(use_angle_cls=True, lang=self.lang, **self.config)
        except Exception as e:
            Logger.error(f"Failed to initialize PaddleOCR: {e}")
            raise

        return self

    def extract(self, image: Image, conf_min: int) -> str:
        try:
            res: OCRResult = self.ocr.predict(
                ImageHandler.paddle_conversion(image)
            )[0]
            if not res:
                raise ValueError("PaddleOCR returned no results")
            text_parts = res["rec_texts"]
            text = ' '.join(text_parts) if text_parts else ''

            res.save_to_json('schedules/image.json')
            return text.strip()

        except Exception as e:
            Logger.error(f"OCR extraction failed: {e}")
            raise

from PIL import Image
from pytesseract import pytesseract

from Interfaces.OCR import OCR
from Utils.ImageHandler import ImageHandler


class TesseractOCR(OCR):
    def __init__(self):
        super().__init__()
        self.__check_tesseract()

    def init(self, debug: bool = False, lang: str = None, config: str = None) -> OCR:
        self.lang = lang or 'fra+eng'
        # -c preserve_interword_spaces=1 add this to the config to have a table like layout
        self.config = config or r'--psm 11 --oem 1 --dpi {dpi}'
        self.debug = debug

        return self

    @classmethod
    def __check_tesseract(cls):
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise RuntimeError(f"Tesseract not found: {e}")

    def extract(self, image: Image, conf_min: int) -> str:

        config = self.config.format(dpi=ImageHandler.get_image_dpi(image))
        data = pytesseract.image_to_data(image, lang=self.lang, config=config,
                                         output_type=pytesseract.Output.DICT)
        text_parts = [d for i, d in enumerate(data['text']) if float(data['conf'][i]) > conf_min if data['conf'][i]]
        text = ' '.join(text_parts) if text_parts else ''

        return text.strip()

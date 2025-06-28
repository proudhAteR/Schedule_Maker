from PIL import Image
from pytesseract import pytesseract

from Interfaces.OCR import OCR
from Utils.FileHandler import FileHandler
from Utils.ImageHandler import ImageHandler


class TesseractOCR(OCR):
    def __init__(self):
        super().__init__()
        self.__check_tesseract()

    def init(self, lang: str = None, debug: bool = False, config: str = None) -> OCR:
        self.lang = lang or 'fra+eng'
        # -c preserve_interword_spaces=1  add this to the config to have a table like layout
        self.config = config or r'--psm 4 --oem 1 --dpi {dpi} -c tessedit_create_tsv=1 -c preserve_interword_spaces=1'
        self.debug = debug

        return self

    @classmethod
    def __check_tesseract(cls):
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise RuntimeError(f"Tesseract not found: {e}")

    def extract(self, image: Image, conf_min: int) -> str:

        self.config.format(dpi=ImageHandler.get_image_dpi(image))
        data = pytesseract.image_to_data(image, lang=self.lang, config=self.config, output_type=pytesseract.Output.DICT)

        FileHandler.convert_ocr_datas(data, 'schedules/image.json')

        return data

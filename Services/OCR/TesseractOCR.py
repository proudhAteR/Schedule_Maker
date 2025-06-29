import random

from PIL import Image
from numpy import ndarray
from pytesseract import pytesseract

from Interfaces.OCR import OCR
from Models.Tables.Box import Box
from Utils.ImageHandler import ImageHandler
from Utils.Logger import Logger


class TesseractOCR(OCR):
    def __init__(self):
        super().__init__()
        self.__check_tesseract()

    def init(self, lang: str = None, debug: bool = False, config: str = None) -> OCR:
        self.lang = lang or 'fra+eng'
        # -c preserve_interword_spaces=1  add this to the config to have a table like layout
        self.config = config or r'--psm 6 --oem 1 --dpi {dpi} -c tessedit_create_tsv=1'
        self.debug = debug

        return self

    @classmethod
    def __check_tesseract(cls):
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise RuntimeError(f"Tesseract not found: {e}")

    def extract(self, src: Box, bit: ndarray, conf_min: int) -> str:
        processed: Image = ImageHandler.image_from_array(
            ImageHandler.crop_image(bit, src)
        )
        self.config.format(
            dpi=ImageHandler.get_image_dpi(processed)
        )

        if self.debug:
            path = f"schedules/debug/{random.random()}.jpg"
            processed.save(path)
            Logger.info(f"Saved processed image to: {path} with size of {processed.size}")

        data = pytesseract.image_to_string(processed, lang=self.lang, config=self.config,
                                           output_type=pytesseract.Output.STRING)

        return data

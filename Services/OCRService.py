from Interfaces.OCR import OCR
from Models.ProcessResult import ProcessResult
from Utils.FileHandler import FileHandler
from Utils.ImageHandler import ImageHandler
from Utils.Logger import Logger
import asyncio


class OCRService:

    def __init__(self, ocr: OCR, lang: str = None, config: str = None, debug: bool = False):
        self.ocr: OCR = ocr.init(lang, debug=debug, config=config)
        self.debug = debug
        self.image = ImageHandler()

    async def extract(self, image_path: str, conf_min: int = 60):
        image_path = FileHandler.in_schedules(image_path)

        if not FileHandler.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        processed = self.__process(image_path)
        table = ImageHandler.get_table(processed.boxes)
        image = self.image.get_bit(processed.image)

        datas = []

        async def ocr_cell(cell):
            if not cell:
                return ' '
            else:
                tasks = [
                    asyncio.to_thread(
                        self.ocr.extract,
                        box, image, conf_min
                    )
                    for box in cell
                ]
                cell_texts = await asyncio.gather(*tasks)
                return ' '.join(cell_texts).strip()

        try:
            # OCR each cell concurrently row by row
            for row in table.cells:
                row_tasks = [
                    ocr_cell(cell) for cell in row
                ]
                row_results = await asyncio.gather(*row_tasks)
                datas.extend(row_results)

            if self.debug:
                Logger.info(f"Extracted {len(datas)} cells")

            return datas

        except Exception:
            raise

    def __process(self, path: str) -> ProcessResult:
        processed = self.image.enhance_image_for_ocr(
            ImageHandler.get_image(path)
        )

        if self.debug:
            processed_path = ImageHandler.get_processed_filename(path)
            processed.image.save(processed_path)
            Logger.info(f"Found {len(processed.boxes)} box(es)")
            Logger.info(f"Saved processed image to: {processed_path}")

        return processed

import os

from PIL.Image import Image
from pdf2image import convert_from_path


class FileService:
    @classmethod
    def exists(cls, path: str):
        return os.path.exists(path)

    @classmethod
    def write(cls, path: str, text: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    @classmethod
    def is_pdf(cls, path):
        try:
            with open(path, 'rb') as f:
                header = f.read(4)
            return header == b'%PDF'
        except IOError:
            return False

    @classmethod
    def convert_pdf_to_images(cls, pdf_path: str, dpi: int = 300) -> Image:
        return convert_from_path(pdf_path, dpi=dpi)[0]

import os

from PIL.Image import Image
from pdf2image import convert_from_path


class FileHandler:
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
    def convert_pdf_to_image(cls, pdf_path: str, dpi: int = 300) -> Image:
        images = convert_from_path(pdf_path, dpi=dpi)
        if not images:
            raise ValueError(f"No pages found in PDF: {pdf_path}")
        return images[0]

    @classmethod
    def in_schedules(cls, path):
        path = 'schedules/' + path
        return path

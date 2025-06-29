from dataclasses import dataclass

from PIL.Image import Image

from Models.Tables.Box import Box

@dataclass
class ProcessResult:
    image: Image
    boxes: list[Box]

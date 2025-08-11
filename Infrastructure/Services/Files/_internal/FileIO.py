import json
from pathlib import Path

import yaml


class FileIO:
    @staticmethod
    def exists(path: str) -> bool:
        return Path(path).exists()

    @staticmethod
    def write(path: str, text: str) -> None:
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        path_obj.write_text(text, encoding="utf-8")

    @staticmethod
    def read_json(file: str):
        path_obj = Path(file)
        if not path_obj.exists():
            return None
        return json.loads(path_obj.read_text(encoding="utf-8"))

    @staticmethod
    def extension_handling(raw: str, ext: str) -> dict:
        match ext:
            case 'json':
                return json.loads(raw) if raw else {}
            case 'yaml', 'yml':
                return yaml.safe_load(raw) if raw else {}
            case _:
                raise ValueError(f"Unsupported config extension: {ext}")

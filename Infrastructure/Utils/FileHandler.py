import json
import os


class FileHandler:
    __ROOT = None

    @classmethod
    def root(cls):
        if cls.__ROOT is None:
            cls.__ROOT = cls.__find_root()
        return cls.__ROOT

    @staticmethod
    def exists(path: str):
        return os.path.exists(path)

    @staticmethod
    def write(path: str, text: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding='utf8') as f:
            f.write(text)

    @classmethod
    def secret_path(cls, file: str):
        return os.path.join(
            cls.root(), 'App', 'secrets', file
        )

    @staticmethod
    def __find_root(marker: str = "pyproject.toml") -> str:
        path = os.path.abspath(__file__)
        while True:
            path = os.path.dirname(path)
            if os.path.exists(os.path.join(path, marker)):
                return path
            if path == os.path.dirname(path):
                raise FileNotFoundError(f"{marker} not found in any parent directory")

    @staticmethod
    def read_json(file: str):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def get_env(key: str):
        return os.getenv(key)

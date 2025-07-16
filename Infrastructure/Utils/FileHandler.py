import os


class FileHandler:
    __ROOT = None

    @classmethod
    def root(cls):
        if cls.__ROOT is None:
            cls.__ROOT = cls.__find_root()
        return cls.__ROOT

    @classmethod
    def exists(cls, path: str):
        return os.path.exists(path)

    @classmethod
    def write(cls, path: str, text: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding='utf8') as f:
            f.write(text)

    @classmethod
    def secret_path(cls, path: str):
        return os.path.join(cls.root(), 'App', 'secrets', path)

    @classmethod
    def __find_root(cls, marker: str = "pyproject.toml") -> str:
        path = os.path.abspath(__file__)
        while True:
            path = os.path.dirname(path)
            if os.path.exists(os.path.join(path, marker)):
                return path
            if path == os.path.dirname(path):
                raise FileNotFoundError(f"{marker} not found in any parent directory")

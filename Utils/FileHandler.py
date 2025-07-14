import os


class FileHandler:
    __BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
        return os.path.join(cls.__BASE_DIR, '..', 'App', 'secrets', path)

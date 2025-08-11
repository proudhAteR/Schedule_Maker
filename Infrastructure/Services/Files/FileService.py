from ._internal.FileIO import FileIO
from ._internal.ProjectPaths import ProjectPaths
from ._internal.Secrets import Secrets


class FileService:
    @staticmethod
    def secret_path(filename: str) -> str:
        return ProjectPaths.secret_path(filename)

    @staticmethod
    def exists(path: str) -> bool:
        return FileIO.exists(path)

    @staticmethod
    def write(path: str, text: str) -> None:
        FileIO.write(path, text)

    @staticmethod
    def read_json(path: str):
        return FileIO.read_json(path)

    @staticmethod
    def load_secret_config(name: str) -> dict:
        return Secrets.load_config(name)

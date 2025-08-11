import importlib.resources as pkg_resources
import os

import Conf
from .._internal.FileIO import FileIO
from .._internal.ProjectPaths import ProjectPaths


class Secrets:
    @staticmethod
    def load_config(name: str, ext: str) -> str:
        if not os.getenv(name):
            cred_filename = f".{name.lower()}.{ext}"
            cred_path = ProjectPaths.root() / "Conf" / cred_filename

            if cred_path.exists():
                with open(cred_path, "r", encoding="utf-8") as f:
                    os.environ[name] = f.read()
            else:
                with pkg_resources.files(Conf).joinpath(cred_filename).open("r", encoding="utf-8") as f:
                    os.environ[name] = f.read()

        return os.getenv(name)

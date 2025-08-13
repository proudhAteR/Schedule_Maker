import importlib.resources as pkg_resources
import os

import Conf
from .._internal.ProjectPaths import ProjectPaths


class Secrets:
    @staticmethod
    def load_config(name: str, ext: str) -> str:
        if not os.getenv(name):
            filename = ProjectPaths.config_name(name, ext)
            path = ProjectPaths.make_hidden(filename)

            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    os.environ[name] = f.read()
            else:
                with pkg_resources.files(Conf).joinpath(filename).open("r", encoding="utf-8") as f:
                    os.environ[name] = f.read()

        return os.getenv(name)
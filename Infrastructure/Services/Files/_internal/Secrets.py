import importlib.resources as pkg_resources
import json
import os

import Conf
from Infrastructure.Services.Files._internal.ProjectPaths import ProjectPaths


class Secrets:
    @staticmethod
    def load_config(name: str) -> dict:
        if not os.getenv(name):
            cred_filename = f".{name.lower()}.json"
            cred_path = ProjectPaths.root() / "Conf" / cred_filename

            if cred_path.exists():
                with open(cred_path, "r", encoding="utf-8") as f:
                    os.environ[name] = f.read()
            else:
                with pkg_resources.files(Conf).joinpath(cred_filename).open("r", encoding="utf-8") as f:
                    os.environ[name] = f.read()

        raw = os.getenv(name)
        return json.loads(raw) if raw else {}

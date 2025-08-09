import json
import os

from Infrastructure.Services.Files._internal.ProjectPaths import ProjectPaths


class Secrets:
    @staticmethod
    def load_config(name: str = "GOOGLE_CREDENTIALS") -> dict:
        if not os.getenv(name):
            cred_path = ProjectPaths.root() / "Conf" / ".google_credentials.json"
            if cred_path.exists():
                with open(cred_path, "r", encoding="utf-8") as f:
                    os.environ[name] = f.read()
            else:
                raise FileNotFoundError(f"Google credentials file not found at {cred_path}")

        raw = os.getenv(name)
        return json.loads(raw) if raw else {}

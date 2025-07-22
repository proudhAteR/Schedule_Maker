import json
import os
from pathlib import Path
from typing import Optional, Any


class FileHandler:
    __ROOT: Optional[Path] = None
    ROOT_ENV_VAR = "SM_ROOT_PATH"

    @classmethod
    def root(cls) -> Path:
        """Get the root directory for the app's files."""
        if cls.__ROOT is None:
            cls.__ROOT = cls.__find_root()
        return cls.__ROOT

    @classmethod
    def __find_root(cls) -> Path:
        """
        Find the root directory by checking:
        1. Environment variable override
        2. Presence of pyproject.toml in parent directories (dev)
        3. Fallback to user home config directory (~/.sm)
        """
        # 1. Check environment variable override
        env_path = os.getenv(cls.ROOT_ENV_VAR)
        if env_path:
            p = Path(env_path).expanduser().resolve()
            if p.exists():
                return p

        # 2. Search for pyproject.toml upwards from this file (dev environment)
        cur = Path(__file__).parent.resolve()
        for parent in [cur] + list(cur.parents):
            if (parent / "pyproject.toml").exists():
                return parent

        # 3. Fallback to user home config directory
        fallback = Path.home() / ".sm"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback

    @classmethod
    def secret_path(cls, filename: str) -> Path:
        """
        Return the full path to a secret file inside the secrets' directory.
        Example: ~/.sm/App/secrets/token.json or project_root/App/secrets/token.json
        """
        return cls.root() / "App" / "secrets" / filename

    @staticmethod
    def exists(path: str | Path) -> bool:
        return Path(path).exists()

    @staticmethod
    def write(path: str | Path, text: str) -> None:
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        path_obj.write_text(text, encoding="utf-8")

    @staticmethod
    def read_json(file: str | Path) -> Optional[Any]:
        path_obj = Path(file)
        if not path_obj.exists():
            return None
        return json.loads(path_obj.read_text(encoding="utf-8"))

    @staticmethod
    def get_config() -> dict:
        """
        Load Google credentials from env var or fallback file.
        Assumes `Conf/.google_credentials.json` exists relative to working dir.
        """
        if not os.getenv("GOOGLE_CREDENTIALS"):
            cred_path = Path("Conf/.google_credentials.json")
            if cred_path.exists():
                with open(cred_path, "r", encoding="utf-8") as f:
                    os.environ["GOOGLE_CREDENTIALS"] = f.read()
            else:
                raise FileNotFoundError(f"Google credentials file not found at {cred_path}")

        raw = os.getenv("GOOGLE_CREDENTIALS")
        return json.loads(raw) if raw else {}

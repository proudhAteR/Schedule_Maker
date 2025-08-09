import os
from pathlib import Path


class ProjectPaths:
    __ROOT = None
    ROOT_ENV_VAR = "SM_ROOT_PATH"

    @classmethod
    def root(cls) -> Path:
        if cls.__ROOT is None:
            cls.__ROOT = cls.__find_root()
        return cls.__ROOT

    @classmethod
    def __find_root(cls) -> Path:
        env_path = os.getenv(cls.ROOT_ENV_VAR)
        if env_path:
            p = Path(env_path).expanduser().resolve()
            if p.exists():
                return p

        cur = Path(__file__).parent.resolve()
        for parent in [cur] + list(cur.parents):
            if (parent / "pyproject.toml").exists():
                return parent

        fallback = Path.home() / ".sm"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback

    @classmethod
    def secret_path(cls, filename: str) -> str:
        return str(cls.root() / "App" / "secrets" / filename)

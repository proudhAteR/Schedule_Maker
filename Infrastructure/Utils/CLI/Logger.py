import threading
from logging import *

from Infrastructure.Utils.CLI.ColorFormatter import ColorFormatter
import Infrastructure.Utils.CLI.LoggerConfig as Config

_ = Config

class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._logger = cls._instance.__get_logger()
        return cls._instance

    @classmethod
    def __get_logger(cls) -> Logger:
        __logger = getLogger()
        if not __logger.handlers:
            __logger.setLevel(INFO)
            handler = StreamHandler()
            formatter = ColorFormatter('%(message)s')
            handler.setFormatter(formatter)
            __logger.addHandler(handler)
            __logger.propagate = False
        return __logger

    @classmethod
    def info(cls, message: str):
        cls.__get_logger().info(message)

    @classmethod
    def success(cls, message: str):
        cls.__get_logger().success(message)

    @classmethod
    def warning(cls, message: str):
        cls.__get_logger().warning(message)

    @classmethod
    def error(cls, message: str):
        cls.__get_logger().error(message)

    @classmethod
    def set_level(cls, level: int):
        cls.__get_logger().setLevel(level)

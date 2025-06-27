from logging import *
import threading


class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Logger, cls).__new__(cls)
                    cls._instance._logger = cls._instance.__get_logger()
        return cls._instance

    @classmethod
    def __get_logger(cls) -> Logger:
        class ColorFormatter(Formatter):
            COLORS = {
                'DEBUG': '\033[94m',  # Blue
                'INFO': '\033[92m',  # Green
                'WARNING': '\033[93m',  # Yellow
                'ERROR': '\033[91m',  # Red
            }
            RESET = '\033[0m'

            def format(self, record):
                level_color = self.COLORS.get(record.levelname, self.RESET)
                log_line = super().format(record)
                return f"{level_color}{log_line}{self.RESET}"

        __logger = getLogger()
        if not __logger.handlers:
            __logger.setLevel(INFO)
            handler = StreamHandler()
            formatter = ColorFormatter('%(asctime)s - [%(levelname)s] - %(message)s')
            handler.setFormatter(formatter)
            __logger.addHandler(handler)
            __logger.propagate = False
        return __logger

    @classmethod
    def info(cls, message: str):
        cls.__get_logger().info(message)

    @classmethod
    def warning(cls, message: str):
        cls.__get_logger().warning(message)

    @classmethod
    def error(cls, message: str):
        cls.__get_logger().error(message)

    @classmethod
    def debug(cls, message: str):
        cls.__get_logger().debug(message)

    @classmethod
    def set_level(cls, level: int):
        cls.__get_logger().setLevel(level)

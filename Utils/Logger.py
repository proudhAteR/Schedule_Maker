import logging

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._logger = cls._instance.__get_logger()
        return cls._instance

    @classmethod
    def __get_logger(cls) -> logging.Logger:
        class ColorFormatter(logging.Formatter):
            COLORS = {
                'DEBUG': '\033[94m',    # Blue
                'INFO': '\033[92m',     # Green
                'WARNING': '\033[93m',  # Yellow
                'ERROR': '\033[91m',    # Red
                'CRITICAL': '\033[95m', # Magenta
            }
            RESET = '\033[0m'

            def format(self, record):
                level_color = self.COLORS.get(record.levelname, self.RESET)
                record.levelname = f"{level_color}{record.levelname}{self.RESET}"
                record.msg = f"{level_color}{record.msg}{self.RESET}"
                return super().format(record)

        logger = logging.getLogger()
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = ColorFormatter('[%(levelname)s] %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.propagate = False
        return logger

    @property
    def logger(self):
        return self._logger
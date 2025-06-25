import logging


class Logger:
    _instance = None

    def __new__(cls, name: str = "schedule_logger"):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._logger = cls._instance.__get_logger(name)
        return cls._instance

    @classmethod
    def __get_logger(cls, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[%(levelname)s] %(asctime)s - %(name)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.propagate = False
        return logger

    @property
    def logger(self):
        return self._logger

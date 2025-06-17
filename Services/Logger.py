import logging

def get_logger(name: str = "schedule_logger") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)  # Set your default level
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(levelname)s] %(asctime)s - %(name)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False  # Avoid duplicate logs if root logger is configured
    return logger
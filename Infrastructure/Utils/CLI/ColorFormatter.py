from logging import Formatter


class ColorFormatter(Formatter):
    COLORS = {
        'INFO': '\033[96m',  # Cyan
        'SUCCESS': '\033[92m',  # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[1;91m',  # Bold Red
    }
    RESET = '\033[0m'

    def format(self, record):
        level_color = self.COLORS.get(record.levelname, self.RESET)
        log_line = super().format(record)
        return f"{level_color}{log_line}{self.RESET}"

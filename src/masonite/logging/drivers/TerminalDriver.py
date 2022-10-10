import logging
import sys

from .BaseDriver import BaseDriver


class ColorFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    magenta = "\x1b[35m"
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    red_fg_yellow_bg = "\x1b[31;103m"
    white_fg_red_bg = "\x1b[37;41m"
    reset = "\x1b[0m"

    def __init__(self, fmt=None, datefmt=None, style="%", validate=True):
        super().__init__(fmt, datefmt, style, validate)
        self.fmt = fmt
        self.style = style
        self.FORMATS = {
            logging.DEBUG: self.magenta + self.fmt + self.reset,
            logging.INFO: self.grey + self.fmt + self.reset,
            logging.NOTICE: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
            logging.ALERT: self.red_fg_yellow_bg + self.fmt + self.reset,
            logging.EMERGENCY: self.white_fg_red_bg + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.datefmt, style=self.style)
        return formatter.format(record)


class TerminalDriver(BaseDriver):
    def __init__(self, application, name, options):
        super().__init__(application, name, options)
        self.logging_handler = logging.StreamHandler(sys.stdout)
        self.logging_handler.setFormatter(ColorFormatter(self.get_format(), style="{"))
        self.logging_logger = logging.getLogger(name)

    def send(self, level, message):
        self.set_logger()
        self.logging_logger.log(
            level, message, extra={"timestamp": self.get_formatted_time()}
        )

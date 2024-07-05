import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from .BaseDriver import BaseDriver
from ...utils.location import base_path


class DailyFileDriver(BaseDriver):
    def __init__(self, application, name, options):
        super().__init__(application, name, options)

        file_path = datetime.now().strftime("%Y-%m-%d") + ".log"

        abs_path = base_path(self.options.get("path", "logs/" + file_path))
        if not os.path.exists(os.path.dirname(abs_path)):
            os.makedirs(os.path.dirname(abs_path))
        self.logging_handler = TimedRotatingFileHandler(
            abs_path,
            when=self.options.get("when", "d"),
            interval=self.options.get("days", 7),
            backupCount=self.options.get("keep", 10),
        )
        self.logging_handler.setFormatter(
            logging.Formatter(self.get_format(), style="{")
        )
        self.logging_logger = logging.getLogger(self.name)

    def send(self, level, message):
        self.set_logger()
        self.logging_logger.log(
            level, message, extra={"timestamp": self.get_formatted_time()}
        )

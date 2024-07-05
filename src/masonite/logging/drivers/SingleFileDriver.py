import logging
import os
from .BaseDriver import BaseDriver
from ...utils.location import base_path


class SingleFileDriver(BaseDriver):
    def __init__(self, application, name, options):
        super().__init__(application, name, options)
        abs_path = base_path(self.options.get("path", "logs/single.log"))
        if not os.path.exists(os.path.dirname(abs_path)):
            os.makedirs(os.path.dirname(abs_path))
        self.logging_handler = logging.FileHandler(
            abs_path,
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

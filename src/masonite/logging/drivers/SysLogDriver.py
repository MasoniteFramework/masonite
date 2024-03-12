import logging
from logging.handlers import SysLogHandler, SYSLOG_UDP_PORT

from .BaseDriver import BaseDriver


class SysLogDriver(BaseDriver):
    def __init__(self, application, name, options):
        super().__init__(application, name, options)
        if self.options.get("host") and self.options.get("port"):
            address = (
                self.options.get("host"),
                self.options.get("port"),
            )
        elif self.options.get("address"):
            address = self.options.get("address")
        else:
            address = ("localhost", SYSLOG_UDP_PORT)
        self.logging_handler = SysLogHandler(address)
        self.logging_handler.setFormatter(
            logging.Formatter(self.get_format(), style="{")
        )
        self.logging_logger = logging.getLogger(self.name)

    def send(self, level, message):
        self.set_logger()
        self.logging_logger.log(
            level, message, extra={"timestamp": self.get_formatted_time()}
        )

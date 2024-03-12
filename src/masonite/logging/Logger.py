import logging
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..foundation import Application

from .LoggerFactory import LoggerFactory
from ..exceptions import InvalidConfigurationSetup


class Logger:
    # 0       Emergency: system is unusable
    # 1       Alert: action must be taken immediately
    # 2       Critical: critical conditions
    # 3       Error: error conditions
    # 4       Warning: warning conditions
    # 5       Notice: normal but significant condition
    # 6       Informational: informational messages
    # 7       Debug: debug-level messages

    def __init__(self, application: "Application", options: dict = {}) -> None:
        self.application = application
        self.drivers = {}
        self.options = options

        # configure python logging module to add new levels
        logging.NOTICE = 25
        logging.ALERT = 60
        logging.EMERGENCY = 70
        new_levels = {
            "notice": logging.NOTICE,
            "alert": logging.ALERT,
            "emergency": logging.EMERGENCY,
        }
        for name, levelno in new_levels.items():
            logging.addLevelName(levelno, name.upper())

        self.levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "notice": logging.NOTICE,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
            "alert": logging.ALERT,
            "emergency": logging.EMERGENCY,
        }

    def get_default_level(self) -> str:
        return self.options.get("channels.default.level")

    def get_default_timezone(self) -> str:
        return self.options.get("channels.default.timezone")

    def get_default_format(self) -> str:
        return self.options.get("channels.default.format")

    def get_default_date_format(self) -> str:
        return self.options.get("channels.default.date_format")

    def add_driver(self, name: str, driver):
        self.drivers.update({name: driver})

    def set_options(self, options: dict) -> "Logger":
        self.options = options
        return self

    def get_driver_from_channel(self, channel: str = None, options: dict = {}):
        if channel is None:
            channel = self.options.get("channels.default.driver")

        # get driver for channel
        driver_name = self.options.get(f"channels.{channel}.driver")
        if not driver_name:
            raise InvalidConfigurationSetup(
                f"No config for channel '{channel}' in config/logging.py !"
            )
        return self.get_driver(
            driver_name, channel, options or self.options.get(f"channels.{channel}")
        )

    def get_driver(self, driver: str, name: str = None, options: dict = {}):
        return self.drivers[driver](self.application, name or driver, options)

    def get_level_name(self, levelno: int) -> str:
        for name, no in self.levels.items():
            if no == levelno:
                return name

    def log(self, level: str, message: str) -> None:
        """Log a message with the given level."""
        return LoggerFactory(self).log(level, message)

    def debug(self, message: str) -> None:
        return LoggerFactory(self).debug(message)

    def info(self, message: str) -> None:
        return LoggerFactory(self).info(message)

    def notice(self, message: str) -> None:
        return LoggerFactory(self).notice(message)

    def warning(self, message: str) -> None:
        return LoggerFactory(self).warning(message)

    def error(self, message: str) -> None:
        return LoggerFactory(self).error(message)

    def critical(self, message: str) -> None:
        return LoggerFactory(self).critical(message)

    def alert(self, message: str) -> None:
        return LoggerFactory(self).alert(message)

    def emergency(self, message: str) -> None:
        return LoggerFactory(self).emergency(message)

    def stack(self, *channels: List[str]) -> "LoggerFactory":
        """On-demand stack channels."""
        return LoggerFactory(self, driver="stack", options={"channels": channels})

    def channel(self, channel: str) -> "LoggerFactory":
        return LoggerFactory(self, channel=channel)

    def build(self, driver: str, options: dict = {}) -> "LoggerFactory":
        return LoggerFactory(self, driver, options=options)

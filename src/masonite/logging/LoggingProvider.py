from ..providers import Provider
from ..facades import Config
from .Logger import Logger
from .drivers import (
    TerminalDriver,
    DailyFileDriver,
    SingleFileDriver,
    StackDriver,
    SysLogDriver,
    SlackDriver,
)
from .LoggerExceptionsListener import LoggerExceptionsListener


class LoggingProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        logger = Logger(self.application).set_options(Config.get("logging"))
        logger.add_driver("terminal", TerminalDriver)
        logger.add_driver("daily", DailyFileDriver)
        logger.add_driver("single", SingleFileDriver)
        logger.add_driver("stack", StackDriver)
        logger.add_driver("syslog", SysLogDriver)
        logger.add_driver("slack", SlackDriver)
        self.application.bind("logger", logger)

        self.application.make("event").listen(
            "masonite.exception.*", [LoggerExceptionsListener]
        )

    def boot(self):
        pass

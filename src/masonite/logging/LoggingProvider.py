from ..providers import Provider
from ..facades import Config
from .Logger import Logger
from .drivers import TerminalDriver, DailyFileDriver, SingleFileDriver, StackDriver


class LoggingProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        logger = Logger(self.application).set_options(Config.get("logging"))
        logger.add_driver("terminal", TerminalDriver)
        logger.add_driver("daily", DailyFileDriver)
        logger.add_driver("single", SingleFileDriver)
        logger.add_driver("stack", StackDriver)
        self.application.bind("logger", logger)

    def boot(self):
        pass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Logger import Logger


class LoggerFactory:
    def __init__(
        self,
        logger: "Logger",
        driver: str = None,
        channel: str = None,
        options: dict = {},
    ) -> None:
        self.logger = logger
        self.driver = driver
        self.channel = channel
        self.options = options

        if driver and not channel:
            self.selected_driver = self.logger.get_driver(driver, options=options)
        # log to default configured channel or given channel
        else:
            self.selected_driver = self.logger.get_driver_from_channel(channel, options)

    def log(self, level: str, message: str) -> None:
        self.selected_driver.log(level, message)

    def debug(self, message: str) -> None:
        self.selected_driver.debug(message)

    def info(self, message: str) -> None:
        self.selected_driver.info(message)

    def notice(self, message: str) -> None:
        self.selected_driver.notice(message)

    def warning(self, message: str) -> None:
        self.selected_driver.warning(message)

    def error(self, message: str) -> None:
        self.selected_driver.error(message)

    def critical(self, message: str) -> None:
        self.selected_driver.critical(message)

    def alert(self, message: str) -> None:
        self.selected_driver.alert(message)

    def emergency(self, message: str) -> None:
        self.selected_driver.emergency(message)

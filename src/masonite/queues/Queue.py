from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..foundation import Application
    from .Queueable import Queueable


class Queue:
    """Queue class allowing to queue jobs to be run asynchronously."""

    def __init__(self, application: "Application", driver_config: dict = {}):
        self.application = application
        self.drivers: dict = {}
        self.driver_config = driver_config
        self.options: dict = {}

    def add_driver(self, name: str, driver: Any) -> None:
        self.drivers.update({name: driver})

    def set_configuration(self, config: dict) -> "Queue":
        self.driver_config = config
        return self

    def get_driver(self, name: str = None) -> Any:
        if name is None:
            return self.drivers[self.driver_config.get("default")]
        return self.drivers[name]

    def get_config_options(self, driver: str = None) -> dict:
        if driver is None:
            return self.driver_config.get(self.driver_config.get("default"), {})

        return self.driver_config.get(driver, {})

    def push(self, *jobs: "Queueable", **options) -> None:
        """Push given job(s) into the queue using the given (or default) queue driver. The queue
        can be given in the options."""
        driver = self.get_driver(options.get("driver"))
        config_options = self.get_config_options(options.get("driver"))
        config_options.update({"queue": options.get("queue", "default")})
        driver.set_options(config_options)
        driver.push(*jobs)

    def consume(self, options: dict):
        """Consume job(s) pushed on the queue using the given (or default) queue driver. The queue
        can be given in the options."""
        driver = self.get_driver(options.get("driver"))
        config_options = self.get_config_options(options.get("driver"))
        config_options.update(options)
        options.update(self.get_config_options(options.get("driver")))
        return driver.set_options(config_options).consume()

    def retry(self, options: dict):
        """Retry failed job(s) on the queue using the given (or default) queue driver. The queue
        can be given in the options."""
        driver = self.get_driver(options.get("driver"))
        config_options = self.get_config_options(options.get("driver"))
        config_options.update(options)
        options.update(self.get_config_options(options.get("driver")))
        return driver.set_options(config_options).retry()

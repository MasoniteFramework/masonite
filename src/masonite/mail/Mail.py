from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..foundation import Application
    from .Mailable import Mailable


class Mail:
    """Mail class which is used to send emails from your application."""

    def __init__(self, application: "Application", driver_config: dict = {}):
        self.application = application
        self.drivers: dict = {}
        self.driver_config = driver_config
        self.options: dict = {}

    def add_driver(self, name: str, driver: Any) -> None:
        self.drivers.update({name: driver})

    def set_configuration(self, config: dict) -> "Mail":
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

    def mailable(self, mailable: "Mailable") -> "Mail":
        """Define the mailable to be sent before calling send()."""
        self.options = mailable.set_application(self.application).build().get_options()
        return self

    def send(self, driver: str = None) -> Any:
        """Send e-mail from your application with the given driver (or default driver)."""
        selected_driver = driver or self.options.get("driver", None)
        config_options = self.get_config_options(selected_driver)
        # if an option has already been defined in a mailable use it
        if self.options.get("from"):
            config_options.pop("from", None)
        self.options.update(config_options)
        return self.get_driver(selected_driver).set_options(self.options).send()

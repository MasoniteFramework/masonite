from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..foundation import Application


class Storage:
    """File storage manager for Masonite handling managing files with different drivers."""

    def __init__(self, application: "Application", store_config: dict = None):
        self.application = application
        self.drivers = {}
        self.store_config = store_config or {}
        self.options = {}

    def add_driver(self, name: str, driver: str):
        self.drivers.update({name: driver})

    def set_configuration(self, config: dict) -> "Storage":
        self.store_config = config
        return self

    def get_driver(self, name: str = None) -> Any:
        if name is None:
            return self.drivers[self.store_config.get("default")]
        return self.drivers[name]

    def get_config_options(self, name: str = None) -> dict:
        if name is None or name == "default":
            return self.store_config.get(self.store_config.get("default"))

        return self.store_config.get(name)

    def disk(self, name: str = "default") -> Any:
        """Get the file manager instance for the given disk name."""
        store_config = self.get_config_options(name)
        driver = self.get_driver(self.get_config_options(name).get("driver"))
        return driver.set_options(store_config)

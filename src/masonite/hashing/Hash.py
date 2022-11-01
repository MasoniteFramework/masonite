from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..foundation import Application


class Hash:
    """Hash class provides secure hashing capabilities with different hashing algorithms. This
    is used e.g. to hash user passwords."""

    def __init__(self, application: "Application", driver_config: dict = {}):
        self.application = application
        self.drivers: dict = {}
        self.driver_config = driver_config
        self.options: dict = {}

    def add_driver(self, name: str, driver: Any) -> None:
        self.drivers.update({name: driver})

    def set_configuration(self, config: dict) -> "Hash":
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

    def make(self, string: str, options: dict = {}, driver: str = None) -> str:
        """Hash the given string and returns the hashed string according to hashing options. The
        string will be hashed with the given driver or the default one."""
        return (
            self.get_driver(driver)
            .set_options(options or self.get_config_options(driver))
            .make(string)
        )

    def make_bytes(self, string: str, options: dict = {}, driver: str = None) -> bytes:
        """Hash the given string and returns the hashed bytes according to hashing options. The
        string will be hashed with the given driver or the default one."""
        return (
            self.get_driver(driver)
            .set_options(options or self.get_config_options(driver))
            .make_bytes(string)
        )

    def check(
        self,
        plain_string: str,
        hashed_string: str,
        options: dict = {},
        driver: str = None,
    ):
        """Verify that the plain string matches the hashed string according to hashing options. The
        comparison will use the given hash driver or the default one."""
        return (
            self.get_driver(driver)
            .set_options(options or self.get_config_options(driver))
            .check(plain_string, hashed_string)
        )

    def needs_rehash(
        self, hashed_string: str, options: dict = {}, driver: str = None
    ) -> bool:
        """Verify if the given hash string needs to be hashed again because options for generating
        the hash have changed. The comparison will use the given hash driver or the default one."""
        return (
            self.get_driver(driver)
            .set_options(options or self.get_config_options(driver))
            .needs_rehash(hashed_string)
        )

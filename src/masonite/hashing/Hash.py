class Hash:
    def __init__(self, application, driver_config=None):
        self.application = application
        self.drivers = {}
        self.driver_config = driver_config or {}
        self.options = {}

    def add_driver(self, name, driver):
        self.drivers.update({name: driver})

    def set_configuration(self, config):
        self.driver_config = config
        return self

    def get_driver(self, name=None):
        if name is None:
            return self.drivers[self.driver_config.get("default")]
        return self.drivers[name]

    def get_config_options(self, driver=None):
        if driver is None:
            return self.driver_config.get(self.driver_config.get("default"), {})
        return self.driver_config.get(driver, {})

    def make(self, string, options={}, driver=None):
        """Hash a string and return as string based on configured hashing protocol."""
        return (
            self.get_driver(driver)
            .set_options(options or self.get_config_options(driver))
            .make(string)
        )

    def make_bytes(self, string, options={}, driver=None):
        """Hash a string and return as bytes based on configured hashing protocol."""
        return (
            self.get_driver(driver)
            .set_options(options or self.get_config_options(driver))
            .make_bytes(string)
        )

    def check(self, plain_string, hashed_string, options={}, driver=None):
        """Verify that a given string matches its hashed version (based on configured hashing protocol)."""
        return (
            self.get_driver(driver)
            .set_options(options or self.get_config_options(driver))
            .check(plain_string, hashed_string)
        )

    def needs_rehash(self, hashed_string, options={}, driver=None):
        """Verify that a given hash needs to be hashed again because parameters for generating
        the hash have changed."""
        return (
            self.get_driver(driver)
            .set_options(options or self.get_config_options(driver))
            .needs_rehash(hashed_string)
        )

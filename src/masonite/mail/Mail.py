class Mail:
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

    def mailable(self, mailable):
        self.options = mailable.set_application(self.application).build().get_options()
        return self

    def send(self, driver=None):
        selected_driver = driver or self.options.get("driver", None)
        config_options = self.get_config_options(selected_driver)
        # if an option has already been defined in a mailable use it
        if self.options.get("from"):
            config_options.pop("from", None)
        self.options.update(config_options)
        return self.get_driver(selected_driver).set_options(self.options).send()

class Storage:
    def __init__(self, application, store_config=None):
        self.application = application
        self.drivers = {}
        self.store_config = store_config or {}
        self.options = {}

    def add_driver(self, name, driver):
        self.drivers.update({name: driver})

    def set_configuration(self, config):
        self.store_config = config
        return self

    def get_driver(self, name=None):
        if name is None:
            return self.drivers[self.store_config.get("default")]
        return self.drivers[name]

    def get_store_config(self, name=None):
        if name is None or name == "default":
            return self.store_config.get(self.store_config.get("default"))

        return self.store_config.get(name)

    def get_config_options(self, name=None):
        if name is None or name == "default":
            return self.store_config.get(self.store_config.get("default"))

        return self.store_config.get(name)

    def disk(self, name="default"):
        store_config = self.get_config_options(name)
        driver = self.get_driver(self.get_config_options(name).get("driver"))
        return driver.set_options(store_config)

class Cache:
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

    def get_config_options(self, name=None):
        if name is None or name == "default":
            return self.store_config.get(self.store_config.get("default"))

        return self.store_config.get(name)

    def store(self, name="default"):
        store_config = self.get_config_options(name)
        driver = self.get_driver(self.get_config_options(name).get("driver"))
        return driver.set_options(store_config)

    def add(self, *args, store=None, **kwargs):
        return self.store(name=store).add(*args, **kwargs)

    def get(self, *args, store=None, **kwargs):
        return self.store(name=store).get(*args, **kwargs)

    def put(self, *args, store=None, **kwargs):
        return self.store(name=store).put(*args, **kwargs)

    def has(self, *args, store=None, **kwargs):
        return self.store(name=store).has(*args, **kwargs)

    def forget(self, *args, store=None, **kwargs):
        return self.store(name=store).forget(*args, **kwargs)

    def increment(self, *args, store=None, **kwargs):
        return self.store(name=store).increment(*args, **kwargs)

    def decrement(self, *args, store=None, **kwargs):
        return self.store(name=store).decrement(*args, **kwargs)

    def flush(self, *args, store=None, **kwargs):
        return self.store(name=store).flush(*args, **kwargs)

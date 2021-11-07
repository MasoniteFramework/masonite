import json


class Session:
    def __init__(self, application, driver_config=None):
        self.application = application
        self.drivers = {}
        self._driver = None
        self.driver_config = driver_config or {}
        self.options = {}
        self.data = {}
        self.added = {}
        self.flashed = {}
        self.deleted = []
        self.deleted_flashed = []

    def add_driver(self, name, driver):
        self.drivers.update({name: driver})

    def driver(self, driver):
        return self.drivers[driver]

    def set_configuration(self, config):
        self.driver_config = config
        return self

    def get_driver(self, name=None):
        if name is None:
            return self.drivers[self.driver_config.get("default")]
        return self.drivers[name]

    def get_config_options(self, driver=None):
        if driver is None:
            return self.driver_config[self.driver_config.get("default")]

        return self.driver_config.get(driver, {})

    # Start of methods
    def start(self, driver=None):
        self.data = {}
        self.added = {}
        self.flashed = {}
        self.deleted = []
        self.deleted_flashed = []
        started_data = self.get_driver(name=driver).start()
        self.data = started_data.get("data")
        self.flashed = started_data.get("flashed")
        return self

    def get_data(self):
        data = self.data
        data.update(self.added)
        data.update(self.flashed)
        for deleted in self.deleted:
            if deleted in data:
                data.pop(deleted)
        for deleted in self.deleted_flashed:
            if deleted in data:
                data.pop(deleted)
        return data

    def save(self, driver=None):
        return self.get_driver(name=driver).save(
            added=self.added,
            deleted=self.deleted,
            flashed=self.flashed,
            deleted_flashed=self.deleted_flashed,
        )

    def set(self, key, value):
        try:
            if isinstance(value, (dict, list, int)) or (
                isinstance(value, str) and value.isnumeric()
            ):
                value = json.dumps(value)
        except json.decoder.JSONDecodeError:
            pass

        return self.added.update({key: value})

    def increment(self, key, count=1):
        return self.set(key, str(int(self.get(key)) + count))

    def decrement(self, key, count=1):
        return self.set(key, str(int(self.get(key)) - count))

    def has(self, key):
        return key in self.added or key in self.flashed

    def get(self, key):
        if key in self.flashed:
            value = self.flashed.get(key)

            try:
                if value is not None:
                    value = json.loads(value)
            except json.decoder.JSONDecodeError:
                pass
            self.flashed.pop(key)
            self.deleted_flashed.append(key)
            return value

        value = self.get_data().get(key)
        try:
            if value is not None:
                value = json.loads(value)
        except json.decoder.JSONDecodeError:
            pass
        return value

    def pull(self, key):
        key_value = self.get(key)
        self.delete(key)
        return key_value

    def flush(self):
        self.deleted += list(self.get_data().keys())

    def delete(self, key):
        self.deleted.append(key)
        if key in self.flashed:
            self.flashed.pop(key)

    def flash(self, key, value):
        """Add temporary data to the session.

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """
        try:
            if isinstance(value, (dict, list, int)) or (
                isinstance(value, str) and value.isnumeric()
            ):
                value = json.dumps(value)
        except json.decoder.JSONDecodeError:
            pass

        self.flashed.update({key: value})

    def all(self):
        """Get all session data.

        Returns:
            dict
        """
        return self.get_data()

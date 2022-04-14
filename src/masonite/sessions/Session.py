import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..foundation import Application


class Session:
    """Session manager which provides a way to store information in a persistent store / backend
    that can be accessed from subsequent requests."""

    def __init__(self, application: "Application", driver_config: dict = {}):
        self.application = application
        self.drivers = {}
        self._driver = None
        self.driver_config = driver_config
        self.options = {}
        self.data = {}
        self.added = {}
        self.flashed = {}
        self.deleted = []
        self.deleted_flashed = []

    def add_driver(self, name: str, driver: Any) -> None:
        """Register a new session driver with the given name."""
        self.drivers.update({name: driver})

    def driver(self, driver: str) -> Any:
        """Get a registered session driver with the given name."""
        return self.drivers[driver]

    def set_configuration(self, config: dict) -> "Session":
        """Set session driver options."""
        self.driver_config = config
        return self

    def get_driver(self, name: str = None) -> Any:
        """Get the default session driver or the driver with the given name."""
        if name is None:
            return self.drivers[self.driver_config.get("default")]
        return self.drivers[name]

    def get_config_options(self, driver: str = None) -> dict:
        """Get the options of the default session driver or of the driver with the given name."""
        if driver is None:
            return self.driver_config[self.driver_config.get("default")]

        return self.driver_config.get(driver, {})

    # Start of methods
    def start(self, driver: str = None) -> "Session":
        """Initialize session."""
        self.data = {}
        self.added = {}
        self.flashed = {}
        self.deleted = []
        self.deleted_flashed = []
        started_data = self.get_driver(name=driver).start()
        self.data = started_data.get("data")
        self.flashed = started_data.get("flashed")
        return self

    def get_data(self) -> dict:
        """Get all session data."""
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

    def save(self, driver: str = None) -> None:
        """Save session data for the default session driver or the given named driver."""
        return self.get_driver(name=driver).save(
            added=self.added,
            deleted=self.deleted,
            flashed=self.flashed,
            deleted_flashed=self.deleted_flashed,
        )

    def set(self, key: str, value: Any) -> None:
        """Save value in default session."""
        try:
            if isinstance(value, (dict, list, int)) or (
                isinstance(value, str) and value.isnumeric()
            ):
                value = json.dumps(value)
        except json.decoder.JSONDecodeError:
            pass

        return self.added.update({key: value})

    def increment(self, key: str, count: int = 1) -> None:
        """Increment session key with given count."""
        return self.set(key, str(int(self.get(key)) + count))

    def decrement(self, key: str, count: int = 1) -> None:
        """Decrement session key with given count."""
        return self.set(key, str(int(self.get(key)) - count))

    def has(self, key: str) -> bool:
        """Check if key is present in default session."""
        return key in self.added or key in self.flashed or key in self.data

    def get(self, key: str) -> Any:
        """Get value of the given key in default session."""
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

    def pull(self, key: str) -> Any:
        """Get and remove value for the given key in session."""
        key_value = self.get(key)
        self.delete(key)
        return key_value

    def flush(self) -> None:
        """Delete all keys from session."""
        self.deleted += list(self.get_data().keys())

    def delete(self, key: str) -> "None|Any":
        """Delete the given key from session."""
        self.deleted.append(key)
        if key in self.flashed:
            self.flashed.pop(key)

    def flash(self, key: str, value: Any) -> None:
        """Save temporary value into session."""
        try:
            if isinstance(value, (dict, list, int)) or (
                isinstance(value, str) and value.isnumeric()
            ):
                value = json.dumps(value)
        except json.decoder.JSONDecodeError:
            pass

        self.flashed.update({key: value})

    def all(self) -> dict:
        """Get all session data."""
        return self.get_data()

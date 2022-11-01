from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from ..foundation import Application


class Cache:
    def __init__(self, application: "Application", store_config: dict = {}):
        self.application = application
        self.drivers: dict = {}
        self.store_config = store_config
        self.options: dict = {}

    def add_driver(self, name: str, driver: Any) -> None:
        self.drivers.update({name: driver})

    def set_configuration(self, config: dict) -> "Cache":
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

    def store(self, name: str = "default") -> Any:
        """Select cache driver by name or use the default cache driver if no name is provided."""
        store_config = self.get_config_options(name)
        driver = self.get_driver(self.get_config_options(name).get("driver"))
        return driver.set_options(store_config)

    def add(
        self, key: str, value: Any, seconds: int = None, store: str = None, **kwargs
    ) -> Any:
        """Add data to cache store. This will either fetch the data already in the cache,
        if it is not expired, or it will insert the new value."""
        return self.store(name=store).add(key, value, seconds, **kwargs)

    def get(self, key: str, default: Any = None, store: str = None, **kwargs) -> Any:
        """Get cache data from cache store. If data is expired it will return None or the default
        value if specified."""
        return self.store(name=store).get(key, default, **kwargs)

    def put(
        self, key: str, value: Any, seconds: int = None, store: str = None, **kwargs
    ) -> Any:
        """Add data to cache store, regardless of if it exists already."""
        return self.store(name=store).put(key, value, seconds, **kwargs)

    def has(self, key: str, store: str = None, **kwargs) -> bool:
        """Check that data exists in cache store and is not expired."""
        return self.store(name=store).has(key, **kwargs)

    def forget(self, key: str, store: str = None, **kwargs) -> Any:
        """Remove data from cache store."""
        return self.store(name=store).forget(key, **kwargs)

    def increment(self, key: str, amount: int = 1, store: str = None, **kwargs) -> Any:
        """Increment an integer data value in cache store."""
        return self.store(name=store).increment(key, amount, **kwargs)

    def decrement(self, key: str, amount: int = 1, store: str = None, **kwargs) -> Any:
        """Decrement an integer data value in cache store."""
        return self.store(name=store).decrement(key, amount, **kwargs)

    def flush(self, store: str = None, **kwargs) -> Any:
        """Delete all data in cache store."""
        return self.store(name=store).flush(**kwargs)

    def remember(
        self, key: str, callable: "Callable", store: str = None, **kwargs
    ) -> Any:
        """Add data to cache store by using a callable."""
        return self.store(name=store).remember(key, callable, **kwargs)

import json
from typing import TYPE_CHECKING, Any, Callable


if TYPE_CHECKING:
    from ...foundation import Application
    from pymemcache.client.base import Client


class MemcacheDriver:
    """Memcached driver storing data in memory."""

    def __init__(self, application: "Application"):
        self.application = application
        self.connection = None

    def set_options(self, options: dict) -> "MemcacheDriver":
        self.options = options
        return self

    def get_connection(self) -> "Client":
        try:
            from pymemcache.client.base import Client
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'pymemcache' library. Run 'pip install pymemcache' to fix this."
            )

        if not self.connection:
            if str(self.options.get("port")) != "0":
                self.connection = Client(
                    f"{self.options.get('host')}:{self.options.get('port')}"
                )
            else:
                self.connection = Client(f"{self.options.get('host')}")

        return self.connection

    def add(self, key: str, value: Any, seconds: int = None) -> Any:
        if self.has(key):
            return self.get(key)

        self.put(key, value, seconds=seconds)
        return value

    def get(self, key: str, default: Any = None, **options) -> Any:
        if not self.has(key):
            return default

        return self.get_value(
            self.get_connection().get(f"{self.get_name()}_cache_{key}")
        )

    def put(self, key: str, value: Any, seconds: int = 0, **options) -> Any:
        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        return self.get_connection().set(
            f"{self.get_name()}_cache_{key}", value, expire=seconds
        )

    def has(self, key: str) -> bool:
        return self.get_connection().get(f"{self.get_name()}_cache_{key}")

    def increment(self, key: str, amount: int = 1) -> Any:
        return self.put(key, str(int(self.get(key)) + amount))

    def decrement(self, key: str, amount: int = 1) -> Any:
        return self.put(key, str(int(self.get(key)) - amount))

    def remember(self, key: str, callable: "Callable") -> Any:
        value = self.get(key)

        if value:
            return value

        callable(self)

    def forget(self, key: str):
        return self.get_connection().delete(f"{self.get_name()}_cache_{key}")

    def flush(self) -> bool:
        return self.get_connection().flush_all()

    def get_name(self) -> str:
        return self.options.get("name")

    def get_value(self, value: Any) -> Any:
        if isinstance(value, bytes):
            value = value.decode("utf-8")

        value = str(value)
        if value.isdigit():
            return str(value)
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            return value

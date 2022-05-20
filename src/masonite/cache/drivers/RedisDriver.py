import json
from typing import TYPE_CHECKING, Any, Callable


if TYPE_CHECKING:
    from ...foundation import Application
    from redis import StrictRedis


class RedisDriver:
    """Redis driver storing data in Redis server."""

    def __init__(self, application: "Application"):
        self.application = application
        self.connection = None

    def set_options(self, options: dict) -> "RedisDriver":
        self.options = options
        return self

    def get_connection(self) -> "StrictRedis":
        try:
            import redis
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'redis' library. Run 'pip install redis' to fix this."
            )

        if not self.connection:
            self.connection = redis.StrictRedis(
                host=self.options.get("host"),
                port=self.options.get("port"),
                password=self.options.get("password"),
                decode_responses=True,
            )

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

    def put(self, key: str, value: Any, seconds: int = None, **options) -> Any:

        time = self.get_expiration_time(seconds)

        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        return self.get_connection().set(
            f"{self.get_name()}_cache_{key}", value, ex=time
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

    def forget(self, key: str) -> Any:
        return self.get_connection().delete(f"{self.get_name()}_cache_{key}")

    def flush(self) -> bool:
        return self.get_connection().flushall()

    def get_name(self) -> str:
        return self.options.get("name")

    def get_expiration_time(self, seconds: int) -> int:
        if seconds is None:
            seconds = 31557600 * 10

        return seconds

    def get_value(self, value: Any) -> Any:
        value = str(value)
        if value.isdigit():
            return str(value)
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            return value

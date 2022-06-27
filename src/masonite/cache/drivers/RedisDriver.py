import json
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from redis import Redis


class RedisDriver:
    def __init__(self, application):
        self.application = application
        self.connection = None
        self._internal_cache: "dict|None" = None

    def set_options(self, options: dict) -> "RedisDriver":
        self.options = options
        return self

    def get_connection(self) -> "Redis":
        try:
            from redis import Redis
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'redis' library. Run 'pip install redis' to fix this."
            )

        if not self.connection:
            self.connection = Redis(
                **self.options.get("options", {}),
                host=self.options.get("host"),
                port=self.options.get("port"),
                password=self.options.get("password"),
                decode_responses=True,
            )

        # populate the internal cache the first time
        # the connection is established
        if self._internal_cache is None and self.connection:
            self._load_from_store(self.connection)

        return self.connection

    def _load_from_store(self, connection: "Redis" = None) -> None:
        """
        copy all the "cache" key value pairs for faster access
        """
        if not connection:
            return

        if self._internal_cache is None:
            self._internal_cache = {}

        cursor = "0"
        prefix = self.get_cache_namespace()
        while cursor != 0:
            cursor, keys = connection.scan(
                cursor=cursor, match=prefix + "*", count=100000
            )
            if keys:
                values = connection.mget(*keys)
                store_data = dict(zip(keys, values))
                for key, value in store_data.items():
                    key = key.replace(prefix, "")
                    value = self.unpack_value(value)
                    self._internal_cache.setdefault(key, value)

    def get_cache_namespace(self) -> str:
        """
        Build the prefix for the key to use in Redis
        """
        namespace = self.options.get("name", None)
        namespace += ":" if namespace else ""
        return f"{namespace}cache:"

    def add(self, key: str, value: Any = None) -> Any:
        if not value:
            return None

        self.put(key, value)
        return value

    def get(self, key: str, default: Any = None, **options) -> Any:
        if default and not self.has(key):
            self.put(key, default, **options)
            return default

        return self._internal_cache.get(key)

    def put(self, key: str, value: Any = None, seconds: int = None, **options) -> Any:
        if not key or value is None:
            return None

        time = self.get_expiration_time(seconds)

        store_value = value
        if isinstance(value, (dict, list, tuple)):
            store_value = json.dumps(value)

        self.get_connection().set(
            f"{self.get_cache_namespace()}{key}", store_value, ex=time
        )

        if not self.has(key):
            self._internal_cache.update({key: value})

    def has(self, key: str) -> bool:
        return key in self._internal_cache

    def increment(self, key: str, amount: int = 1) -> int:
        value = int(self.get(key)) + amount
        self.put(key, value)
        return value

    def decrement(self, key: str, amount: int = 1) -> int:
        value = int(self.get(key)) - amount
        self.put(key, value)
        return value

    def remember(self, key: str, callable):
        value = self.get(key)

        if value:
            return value

        callable(self)

    def forget(self, key: str) -> None:
        self.get_connection().delete(f"{self.get_cache_namespace()}{key}")
        self._internal_cache.pop(key)

    def flush(self) -> None:
        return self.get_connection().flushall()

    def get_expiration_time(self, seconds: int) -> int:
        if seconds is None:
            seconds = 31557600 * 10

        return seconds

    def unpack_value(self, value: Any) -> Any:
        value = str(value)
        if value.isdigit():
            return str(value)
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            return value

import json
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from redis import Redis


class RedisDriver:
    def __init__(self, application):
        self.application = application
        self.connection = None
        self.options = None
        self._internal_cache: dict = None

    def set_options(self, options: dict) -> "RedisDriver":
        self.options = options
        return self

    def get_connection(self) -> "Redis":
        if self.connection:
            return self.connection

        try:
            from redis import Redis
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'redis' library. Run 'pip install redis' to fix this."
            )

        self.connection = Redis(
            **self.options.get("options", {}),
            host=self.options.get("host"),
            port=self.options.get("port"),
            password=self.options.get("password"),
            decode_responses=True,
        )

        return self.connection

    def _load_from_store(self) -> None:
        """
        copy all the "cache" key value pairs for faster access
        """
        if self._internal_cache is not None:
            return

        self._internal_cache = {}

        cursor = "0"
        prefix = self.get_cache_namespace()
        while cursor != 0:
            cursor, keys = self.get_connection().scan(
                cursor=cursor, match=prefix + "*", count=100000
            )
            if keys:
                values = self.get_connection().mget(*keys)
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
        if value is None:
            return None

        self.put(key, value)
        return value

    def get(self, key: str, default: Any = None, **options) -> Any:
        self._load_from_store()
        if default and not self.has(key):
            return default

        return self._internal_cache.get(key)

    def put(self, key: str, value: Any = None, seconds: int = None, **options) -> Any:
        if not key or value is None:
            return None

        time = seconds or self.get_default_timeout()

        store_value = value
        if isinstance(value, (dict, list, tuple)):
            store_value = json.dumps(value)
        elif isinstance(value, int):
            store_value = str(value)

        self._load_from_store()
        self.get_connection().set(
            f"{self.get_cache_namespace()}{key}", store_value, ex=time
        )
        self._internal_cache.update({key: value})

    def has(self, key: str) -> bool:
        self._load_from_store()
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

        return self.get(key)

    def forget(self, key: str) -> None:
        if not self.has(key):
            return
        self.get_connection().delete(f"{self.get_cache_namespace()}{key}")
        self._internal_cache.pop(key)

    def flush(self) -> None:
        flushed = self.get_connection().flushall()
        if flushed:
            self._internal_cache = None

        return flushed

    def get_default_timeout(self) -> int:
        # if unset default timeout of cache vars is 1 month
        return int(self.options.get("timeout", 60 * 60 * 24 * 30))

    def unpack_value(self, value: Any) -> Any:
        value = str(value)
        if value.isdigit():
            return int(value)

        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            return value

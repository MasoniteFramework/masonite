import json
from typing import TYPE_CHECKING, Any


from ..BaseDriver import BaseDriver
from ...validation import MessageBag

if TYPE_CHECKING:
    from ...foundation import Application


class RedisDriver(BaseDriver):
    """Session driver used to store data in Redis."""

    def __init__(self, application: "Application"):
        super().__init__(application)
        self.connection = None

    def get_connection(self):
        try:
            import redis
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'redis' library. Run 'pip install redis' to fix this."
            )

        if not self.connection:
            self.connection = redis.Redis(
                **self.options.get("options", {}),
                host=self.options.get("host"),
                port=self.options.get("port", 6379),
                password=self.options.get("password", None),
                decode_responses=True
            )

        return self.connection

    def start(self) -> dict:
        data = {}
        flashed = {}

        session_data = {}
        cursor = "0"
        session_prefix = self.get_session_namespace() + "*"
        while cursor != 0:
            cursor, keys = self.get_connection().scan(
                cursor=cursor, match=session_prefix, count=100000
            )
            if keys:
                values = self.get_connection().mget(*keys)
                # values = map(int, values)
                session_data.update(dict(zip(keys, values)))

        data_prefix = self.get_data_prefix()
        flash_prefix = self.get_flash_prefix()
        for key, value in session_data.items():
            if key.startswith(data_prefix):
                data.update({key.replace(data_prefix, ""): value})
            elif key.startswith(flash_prefix):
                flashed.update({key.replace(flash_prefix, ""): value})

        return {"data": data, "flashed": flashed}

    def save(
        self,
        added: dict = None,
        deleted: list = None,
        flashed: dict = None,
        deleted_flashed: list = None,
    ) -> None:
        if added is None:
            added = {}
        if deleted is None:
            deleted = []
        if flashed is None:
            flashed = {}
        if deleted_flashed is None:
            deleted_flashed = []

        for key, value in flashed.items():
            if isinstance(value, (MessageBag)):
                value = value.json()
            self.set(f"{self.get_flash_prefix()}{key}", value)

        for key, value in added.items():
            self.set(f"{self.get_data_prefix()}{key}", value)

        for key in deleted:
            self.delete(f"{self.get_data_prefix()}{key}")

        for key in deleted_flashed:
            self.delete(f"{self.get_flash_prefix()}{key}")

    def get_session_namespace(self, session_id: str = None) -> str:
        if not session_id:
            request = self.application.make("request")
            session_id = request.cookie("SESSID")
        namespace = self.options.get("namespace", "")
        namespace += ":" if namespace else ""
        return f"{namespace}session:{session_id}:"

    def get_data_prefix(self) -> str:
        return f"{self.get_session_namespace()}data:"

    def get_flash_prefix(self) -> str:
        return f"{self.get_session_namespace()}flash:"

    def helper(self) -> "RedisDriver":
        """Use to create builtin helper function."""
        return self

    def get(self, key: str, default: str = None) -> str:
        if not self.has(key):
            return default
        return self.get_value(self.get_connection().get(key))

    def set(self, key: str, value: Any, time: int = None):
        time = time or self.get_timeout()

        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        return self.get_connection().set(key, value, ex=time)

    def has(self, key: str) -> bool:
        return self.get_connection().get(key)

    def delete(self, key: str):
        return self.get_connection().delete(key)

    def flush(self, session_id: str = None) -> None:
        """
        Clears all data for the current (or provided) session id
        """

        cursor = "0"
        session_prefix = self.get_session_namespace(session_id) + "*"
        connection = self.get_connection()
        while cursor != 0:
            cursor, keys = connection.scan(
                cursor=cursor, match=session_prefix, count=100000
            )
            if keys:
                connection.delete(*keys)

    def get_timeout(self) -> int:
        # default timeout of session vars is 24 hrs
        return int(self.options.get("timeout", 60 * 60 * 24))

    def get_value(self, value: Any) -> str:
        value = str(value)
        if value.isdigit():
            return str(value)
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            return value

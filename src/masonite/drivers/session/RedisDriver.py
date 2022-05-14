import json
from typing import TYPE_CHECKING

from ..BaseDriver import BaseDriver
from ...validation import MessageBag

if TYPE_CHECKING:
    from ...foundation import Application
    from ...request import Request


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
            driver_config = self.options['driver_config']
            driver_config.update({"decode_responses": True})
            self.connection = redis.StrictRedis(
                **driver_config,
            )

        return self.connection

    def start(self) -> dict:
        data = {}
        flashed = {}

        session_data = {}
        cursor = '0'
        session_prefix = self.get_session_namespace() + '*'
        while cursor != 0:
            cursor, keys = self.get_connection().scan(cursor=cursor, match=session_prefix, count=100000)
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
        self, added=None, deleted=None, flashed=None, deleted_flashed=None
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
            self.put(f"{self.get_flash_prefix()}{key}", value)

        for key, value in added.items():
            self.put(f"{self.get_data_prefix()}{key}", value)

        for key in deleted:
            self.forget(f"{self.get_data_prefix()}{key}")

        for key in deleted_flashed:
            self.forget(f"{self.get_flash_prefix()}{key}")

    def get_session_namespace(self, session_id=None):
        if not session_id:
            request = self.application.make("request")
            session_id = request.cookie("SESSID")
        ns = self.options.get("namespace", "")
        ns += ":" if ns else ""
        return f"{ns}session:{session_id}:"

    def get_data_prefix(self):
        return f"{self.get_session_namespace()}data:"

    def get_flash_prefix(self):
        return f"{self.get_session_namespace()}flash:"

    def helper(self) -> "RedisDriver":
        """Use to create builtin helper function."""
        return self

    def get(self, key, default=None, **options):
        if not self.has(key):
            return default
        return self.get_value(
            self.get_connection().get(key)
        )

    def put(self, key, value, **options):
        time = self.get_timeout()

        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        return self.get_connection().set(key, value, ex=time)

    def has(self, key):
        return self.get_connection().get(key)

    def forget(self, key):
        return self.get_connection().delete(key)

    def flush(self, session_id=None):
        """
        Clears all data for the current session id
        """

        cursor = '0'
        session_prefix = self.get_session_namespace(session_id) + '*'
        connection = self.get_connection()
        while cursor != 0:
            cursor, keys = connection.scan(cursor=cursor, match=session_prefix, count=100000)
            if keys:
                connection.delete(*keys)

    def get_timeout(self):
        # default timeout of session vars is 24 hrs
        return self.options.get("timeout", 60 * 60 * 24)

    def get_value(self, value):
        value = str(value)
        if value.isdigit():
            return str(value)
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            return value

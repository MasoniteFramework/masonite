import json


class MemcacheDriver:
    def __init__(self, application):
        self.application = application
        self.connection = None

    def set_options(self, options):
        self.options = options
        return self

    def get_connection(self):
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

    def add(self, key, value):
        if self.has(key):
            return self.get(key)

        self.put(key, value)
        return value

    def get(self, key, default=None, **options):
        if not self.has(key):
            return default

        return self.get_value(
            self.get_connection().get(f"{self.get_name()}_cache_{key}")
        )

    def put(self, key, value, seconds=0, **options):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        return self.get_connection().set(
            f"{self.get_name()}_cache_{key}", value, expire=seconds
        )

    def has(self, key):
        return self.get_connection().get(f"{self.get_name()}_cache_{key}")

    def increment(self, key, amount=1):
        return self.put(key, str(int(self.get(key)) + amount))

    def decrement(self, key, amount=1):
        return self.put(key, str(int(self.get(key)) - amount))

    def remember(self, key, callable):
        value = self.get(key)

        if value:
            return value

        callable(self)

    def forget(self, key):
        return self.get_connection().delete(f"{self.get_name()}_cache_{key}")

    def flush(self):
        return self.get_connection().flush_all()

    def get_name(self):
        return self.options.get("name")

    def get_value(self, value):
        if isinstance(value, bytes):
            value = value.decode("utf-8")

        value = str(value)
        if value.isdigit():
            return str(value)
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            return value

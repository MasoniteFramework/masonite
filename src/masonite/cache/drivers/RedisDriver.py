import json


class RedisDriver:
    def __init__(self, application):
        self.application = application
        self.connection = None

    def set_options(self, options):
        self.options = options
        return self

    def get_connection(self):
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

    def put(self, key, value, seconds=None, **options):

        time = self.get_expiration_time(seconds)

        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        return self.get_connection().set(
            f"{self.get_name()}_cache_{key}", value, ex=time
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
        return self.get_connection().flushall()

    def get_name(self):
        return self.options.get("name")

    def get_expiration_time(self, seconds):
        if seconds is None:
            seconds = 31557600 * 10

        return seconds

    def get_value(self, value):
        value = str(value)
        if value.isdigit():
            return str(value)
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            return value

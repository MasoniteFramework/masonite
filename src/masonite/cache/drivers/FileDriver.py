import os
from ...utils.filesystem import make_full_directory, modified_date
from pathlib import Path
import pendulum
import json
import glob


class FileDriver:
    def __init__(self, application):
        self.application = application

    def set_options(self, options):
        self.options = options
        if options.get("location"):
            make_full_directory(options.get("location"))
        return self

    def add(self, key, value, seconds=None):
        exists = self.get(key)
        if exists:
            return exists

        return self.put(key, str(value), seconds=seconds)

    def get(self, key, default=None, **options):
        if not self.has(key):
            return None

        modified_at = self.get_modified_at(os.path.join(self._get_directory(), key))

        with open(os.path.join(self._get_directory(), key), "r") as f:
            value = f.read()

            if modified_at.add(seconds=self.get_cache_expiration(value)).is_past():
                self.forget(key)
                return default

            value = self.get_value(value)

        return value

    def put(self, key, value, seconds=None, **options):

        time = self.get_expiration_time(seconds)

        if isinstance(value, (dict,)):
            value = json.dumps(value)

        with open(os.path.join(self._get_directory(), key), "w") as f:
            f.write(f"{time}:{value}")

        return value

    def has(self, key):
        return Path(os.path.join(self._get_directory(), key)).exists()

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
        try:
            os.remove(os.path.join(self._get_directory(), key))
            return True
        except FileNotFoundError:
            return False

    def flush(self):
        files = glob.glob(f"{self._get_directory()}/*")
        for f in files:
            os.remove(f)

    def _get_directory(self):
        return self.options.get("location")

    def get_modified_at(self, filename):
        return pendulum.from_timestamp(modified_date(filename))

    def get_expiration_time(self, seconds):
        if seconds is None:
            seconds = 31557600 * 10

        return seconds

    def get_value(self, value):
        value = str(value.split(":", 1)[1])
        if value.isdigit():
            return str(value)
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            return value

    def get_cache_expiration(self, value):
        return int(value.split(":", 1)[0])

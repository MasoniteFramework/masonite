import pendulum
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from ..foundation import Application
    from .limiters import Limiter


class RateLimiter:
    def __init__(self, application: "Application"):
        self.application = application
        self.limiters: dict = {}

    def register(self, name, callback: "Limiter") -> "RateLimiter":
        self.limiters[name] = callback
        return self

    @property
    def cache(self) -> Any:
        """Get default cache driver"""
        return self.application.make("cache").store()

    def attempts(self, key: str) -> int:
        key = self.clean_key(key)
        return int(self.cache.get(key, default=0))

    def clean_key(self, key: str) -> str:
        """Clean the rate limiter key from unicode characters."""
        if isinstance(key, bytes):
            return key.decode("utf-8")
        return key

    def get_limiter(self, name: str) -> "Limiter":
        return self.limiters[name]

    def attempt(self, key: str, callback: Callable, max_attempts: int, delay: int = 60):
        # don't execute callback if key limited
        if self.too_many_attempts(key, max_attempts):
            return False

        result = callback()
        self.hit(key, delay)
        return result

    def too_many_attempts(self, key: str, max_attempts: int) -> bool:
        key = self.clean_key(key)
        if self.attempts(key) >= max_attempts:
            # trigger remove of cache value if needed
            self.cache.get(f"{key}:timer")
            if self.cache.has(f"{key}:timer"):
                return True
            self.reset_attempts(key)
        return False

    def hit(self, key: str, delay: int) -> int:
        key = self.clean_key(key)
        # store timestamp when key limit be available again
        available_at = pendulum.now().add(seconds=delay).int_timestamp
        self.cache.add(f"{key}:timer", available_at, delay)
        # ensure key exists
        self.cache.add(key, 0, delay)
        hits = self.cache.increment(key)
        return hits

    def reset_attempts(self, key: str) -> bool:
        key = self.clean_key(key)
        return self.cache.put(key, 0)

    def clear(self, key: str):
        key = self.clean_key(key)
        self.cache.forget(key)
        self.cache.forget(f"{key}:timer")

    def available_at(self, key: str) -> int:
        """Get UNIX integer timestamp at which key will be available again."""
        key = self.clean_key(key)
        timestamp = int(self.cache.get(f"{key}:timer", 0))
        return timestamp

    def available_in(self, key: str) -> int:
        """Get seconds in which key will be available again."""
        timestamp = self.available_at(key)
        if not timestamp:
            return 0
        else:
            return max(0, timestamp - pendulum.now().int_timestamp)

    def remaining(self, key: str, max_attempts: int) -> int:
        """Get remaining attempts before limitation."""
        key = self.clean_key(key)
        return max_attempts - self.attempts(key)

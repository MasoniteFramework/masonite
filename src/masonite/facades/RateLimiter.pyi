from typing import Any, Callable

class RateLimiter:
    """Rate Limiter facades to add rate limiting to your functions."""

    def attempt(
        key: str, callback: Callable, max_attempts: int, delay: int = 60
    ) -> Any:
        """Try to execute the given callback if not limited by the 'key' rate limiter."""
        ...

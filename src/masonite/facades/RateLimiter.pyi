from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..rates.limiters import Limiter

class RateLimiter:
    """Rate Limiter facades to add rate limiting to your functions."""

    def register(self, name, callback: "Limiter") -> "RateLimiter":
        """Register a new rate limiter with the given name"""
        ...
    def attempts(self, key: str) -> int:
        """Get number of attempts left for a given rate limiter key."""
        ...
    def get_limiter(self, name: str) -> "Limiter":
        """Get rate limiter registered with the given name."""
        ...
    def attempt(
        key: str, callback: Callable, max_attempts: int, delay: int = 60
    ) -> Any:
        """Try to execute the given callback if not limited by the 'key' rate limiter."""
        ...
    def too_many_attempts(self, key: str, max_attempts: int) -> bool:
        """Check if given rate limiter key got more (or equal) attempts than max_attempts."""
        ...
    def hit(self, key: str, delay: int) -> int:
        """Add one attempt for the given key."""
        ...
    def reset_attempts(self, key: str) -> bool:
        """Reset attempts count to 0 for the given key."""
        ...
    def clear(self, key: str):
        """Clear all data of the given rate limiter key."""
        ...
    def available_at(self, key: str) -> int:
        """Get UNIX integer timestamp at which rate limiter key will be available again."""
        ...
    def available_in(self, key: str) -> int:
        """Get seconds in which rate limiter key will be available again."""
        ...
    def remaining(self, key: str, max_attempts: int) -> int:
        """Get remaining attempts before given rate limiter key is limited regarding max_attempts limit."""
        ...

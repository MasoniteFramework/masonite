from .Limit import Limit
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..request import Request


class Limiter:
    def __init__(self):
        pass

    def allow(self, request: "Request"):
        pass


class GlobalLimiter(Limiter):
    """Apply a global limit"""

    def __init__(self, limit: str):
        self.limit = limit

    def allow(self, request: "Request") -> "Limit":
        return Limit.from_str(self.limit)


class UnlimitedLimiter(Limiter):
    def allow(self, request: "Request") -> "Limit":
        return Limit.unlimited()


class GuestsOnlyLimiter(Limiter):
    """Apply a limit for guests only."""

    def __init__(self, limit: str):
        self.limit = limit

    def allow(self, request: "Request") -> "Limit":
        if request.user():
            return Limit.unlimited()
        else:
            return Limit.from_str(self.limit).by(request.ip())

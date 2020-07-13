"""Guard Middleware."""

from ..auth import Auth
from ..helpers import config


class GuardMiddleware:
    """Middleware to switch the guard"""

    def __init__(self, auth: Auth):
        self.auth = auth

    def before(self, guard):
        """Sets specified guard for the request.

        Arguments:
            guard {string} -- The key of the guard to set.
        """
        self.auth.set(guard)

    def after(self, _):
        """Sets the default guard back after the request.

        Arguments:
            _ {ignored} -- ignored
        """
        self.auth.set(config('auth.auth.defaults.guard'))

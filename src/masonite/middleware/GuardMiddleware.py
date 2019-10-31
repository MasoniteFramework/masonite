"""CSRF Middleware."""

from ..auth import Auth
from ..helpers import config

class GuardMiddleware:
    """Middleware to switch the guard"""

    def __init__(self, auth: Auth):
        self.auth = auth

    def before(self, guard):
        self.auth.set(guard)

    def after(self, guard):
        self.auth.set(config('auth.auth.defaults.guard'))

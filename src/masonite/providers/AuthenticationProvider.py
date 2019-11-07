"""An Authentication Service Provider."""

from ..auth.guards import Guard, WebGuard
from ..auth import Auth
from ..helpers import config
from ..provider import ServiceProvider


class AuthenticationProvider(ServiceProvider):

    wsgi = False

    def register(self):
        guard = Guard(self.app)
        guard.register_guard('web', WebGuard)
        self.app.simple(guard)
        self.app.swap(Auth, guard)

    def boot(self, auth: Auth):
        auth.set(config('auth.auth.defaults.guard'))

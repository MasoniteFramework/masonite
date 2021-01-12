"""A Csrf Service Provider."""

from ..auth import Csrf
from ..provider import ServiceProvider


class CsrfProvider(ServiceProvider):

    wsgi = True

    def register(self):
        pass

    def boot(self):
        self.app.bind("Csrf", Csrf(self.app.make("Request")))
        pass

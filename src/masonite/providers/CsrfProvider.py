"""A Csrf Service Provider."""

from ..auth import Csrf
from ..provider import ServiceProvider


class CsrfProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('Csrf', Csrf(self.app.make('Request')))

    def boot(self):
        pass

"""A Csrf Service Provider."""

from masonite.auth import Csrf
from masonite.provider import ServiceProvider


class CsrfProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('Csrf', Csrf(self.app.make('Request')))

    def boot(self):
        pass

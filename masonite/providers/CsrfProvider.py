""" A Csrf Service Provider """
from masonite.provider import ServiceProvider
from masonite.auth.Csrf import Csrf


class CsrfProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('Csrf', Csrf(self.app.make('Request')))

    def boot(self):
        pass

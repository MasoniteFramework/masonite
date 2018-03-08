""" A Csrf Service Provider """
from masonite.provider import ServiceProvider
from masonite.auth.Csrf import Csrf


class CsrfProvider(ServiceProvider):

    wsgi = True

    def register(self):
        self.app.bind('CSRF', Csrf(self.app.make('Request')))

    def boot(self, View, ViewClass, Request):
        pass

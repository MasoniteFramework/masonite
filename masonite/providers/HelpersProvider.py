""" A SassProvider Service Provider """
import builtins
import os

from masonite.provider import ServiceProvider


class HelpersProvider(ServiceProvider):

    wsgi = False

    def register(self):
        pass

    def boot(self, View, ViewClass, Request):
        """ Add helper functions to Masonite """
        builtins.view = View
        builtins.request = Request.helper
        builtins.auth = Request.user
        builtins.container = self.app.helper
        builtins.env = os.getenv
        builtins.resolve = self.app.resolve

        ViewClass.share({'request': Request.helper, 'auth': Request.user})

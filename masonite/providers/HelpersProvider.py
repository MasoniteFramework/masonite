''' A SassProvider Service Provider '''
from masonite.provider import ServiceProvider
import builtins
import os

class HelpersProvider(ServiceProvider):

    wsgi = False

    def register(self):
        pass

    def boot(self, View, ViewClass, Request):
        ''' Add helper functions to Masonite '''
        builtins.view = View
        builtins.request = Request.helper
        builtins.auth = Request.user
        builtins.container = self.app.helper
        builtins.env = os.getenv
        builtins.resolve = self.app.resolve

        ViewClass.share({'request': Request.helper, 'auth': Request.user})

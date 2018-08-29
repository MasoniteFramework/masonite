""" A SassProvider Service Provider """

import builtins
import os

from masonite.helpers.view_helpers import back, set_request_method
from masonite.provider import ServiceProvider
from masonite.view import View
from masonite.request import Request


class HelpersProvider(ServiceProvider):

    wsgi = False

    def register(self):
        pass

    def boot(self, view: View, request: Request):
        """ Add helper functions to Masonite """
        builtins.view = view.render
        builtins.request = request.helper
        builtins.auth = request.user
        builtins.container = self.app.helper
        builtins.env = os.getenv
        builtins.resolve = self.app.resolve
        builtins.route = request.route

        view.share(
            {
                'request': request.helper,
                'auth': request.user,
                'request_method': set_request_method,
                'route': request.route,
                'back': back
            }
        )

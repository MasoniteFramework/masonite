"""A SassProvider Service Provider."""

import builtins
import os

from masonite.exception_handler import DD
from masonite.helpers.view_helpers import back, set_request_method, hidden
from masonite.helpers.sign import sign, unsign, decrypt, encrypt
from masonite.helpers import config, optional
from masonite.provider import ServiceProvider
from masonite.view import View
from masonite.request import Request
from masonite.managers import MailManager


class HelpersProvider(ServiceProvider):

    wsgi = False

    def register(self):
        pass

    def boot(self, view: View, request: Request):
        """Add helper functions to Masonite."""
        builtins.view = view.render
        builtins.request = request.helper
        builtins.auth = request.user
        builtins.container = self.app.helper
        builtins.env = os.getenv
        builtins.resolve = self.app.resolve
        builtins.route = request.route
        if self.app.has(MailManager):
            builtins.mail_helper = self.app.make(MailManager).helper
        builtins.dd = DD(self.app).dump

        view.share(
            {
                'request': request.helper,
                'auth': request.user,
                'request_method': set_request_method,
                'route': request.route,
                'back': back,
                'sign': sign,
                'unsign': unsign,
                'decrypt': decrypt,
                'encrypt': encrypt,
                'config': config,
                'optional': optional,
                'dd': builtins.dd,
                'hidden': hidden,
                'exists': view.exists,
                'cookie': request.get_cookie,
                'url': lambda name, params={}: request.route(name, params, full=True)
            }
        )

"""A Helpers Service Provider."""

import builtins
import os

from ..exception_handler import DD
from ..helpers.view_helpers import back, set_request_method, hidden, old
from ..helpers.sign import sign, unsign, decrypt, encrypt
from ..helpers import config, optional
from ..provider import ServiceProvider
from ..view import View
from ..request import Request
from ..managers import MailManager


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
                'url': lambda name, params={}: request.route(name, params, full=True),
                'old': old
            }
        )

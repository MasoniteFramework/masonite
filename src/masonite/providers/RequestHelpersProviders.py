"""A Helpers Service Provider."""

import builtins
import os

from ..provider import ServiceProvider
from ..view import View
from ..request import Request


class RequestHelpersProvider(ServiceProvider):
    def register(self):
        pass

    def boot(self, view: View, request: Request):
        """Add helper functions to Masonite."""
        builtins.auth = request.user
        builtins.route = request.route

        view.share(
            {
                "request": request.helper,
                "auth": request.user,
                "route": request.route,
                "cookie": request.get_cookie,
                "url": lambda name, params={}: request.route(name, params, full=True),
            }
        )

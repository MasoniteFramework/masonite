import builtins
from markupsafe import Markup

from ..providers import Provider
from ..configuration import config
from ..helpers import UrlsHelper, MixHelper, optional
from ..facades import Dump


class HelpersProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        builtins.resolve = self.application.resolve
        builtins.container = lambda: self.application
        self.application.bind("url", UrlsHelper(self.application))

    def boot(self):
        request = self.application.make("request")

        self.application.make("view").share(
            {
                "request": lambda: request,
                "session": lambda: request.app.make("session"),
                "auth": request.user,
                "cookie": request.cookie,
                "back": lambda url=request.get_path_with_query(): (
                    Markup(f"<input type='hidden' name='__back' value='{url}' />")
                ),
                "method": lambda method: (
                    Markup(f"<input type='hidden' name='__method' value='{method}' />")
                ),
                "dd": Dump.dd,
                "can": self.application.make("gate").allows,
                "cannot": self.application.make("gate").denies,
            }
        )

import builtins
from markupsafe import Markup

from ..providers import Provider
from ..configuration import config
from ..helpers import UrlsHelper, MixHelper


class HelpersProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        builtins.resolve = self.application.resolve
        builtins.container = lambda: self.application
        self.application.bind("url", UrlsHelper(self.application))

    def boot(self):
        request = self.application.make("request")
        urls_helper = self.application.make("url")

        self.application.make("view").share(
            {
                "request": lambda: request,
                "session": lambda: request.app.make("session"),
                "auth": request.user,
                "cookie": request.cookie,
                "back": lambda url=request.get_path_with_query(): (
                    Markup(f"<input type='hidden' name='__back' value='{url}' />")
                ),
                "asset": urls_helper.asset,
                "url": urls_helper.url,
                "mix": MixHelper(self.application).url,
                "route": urls_helper.route,
                "config": config,
                "can": self.application.make("gate").allows,
                "cannot": self.application.make("gate").denies,
            }
        )

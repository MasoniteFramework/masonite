from ..views import View
from .Provider import Provider
from ..helpers import optional, config, url, mix
from ..facades import Dump
from markupsafe import Markup


class ViewProvider(Provider):
    def __init__(self, app):
        self.application = app

    def register(self):
        view = View(self.application)
        view.add_location(self.application.make("views.location"))
        self.application.bind("view", view)

    def boot(self):
        """Register all needed helpers in view as well as some important services."""
        request = self.application.make("request")
        view = self.application.make("view")
        view.share(
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
                "optional": optional,
                "config": config,
                "asset": url.asset,
                "mix": mix.url,
                "url": url.url,
                "route": url.route,
                "config": config,
                "exists": view.exists,
                "optional": optional,
            }
        )

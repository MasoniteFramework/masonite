from ..views import View
from .Provider import Provider
from ..helpers import UrlsHelper, MixHelper, optional
from ..configuration import config


class ViewProvider(Provider):
    def __init__(self, app):
        self.application = app

    def register(self):
        view = View(self.application)
        view.add_location(self.application.make("views.location"))

        self.application.bind("url", UrlsHelper(self.application))
        urls_helper = self.application.make("url")

        view.share(
            {
                "asset": urls_helper.asset,
                "mix": MixHelper(self.application).url,
                "url": urls_helper.url,
                "route": urls_helper.route,
                "config": config,
                "exists": view.exists,
                "optional": optional,
            }
        )

        self.application.bind("view", view)

    def boot(self):
        pass

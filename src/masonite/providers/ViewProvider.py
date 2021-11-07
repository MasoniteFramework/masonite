from ..views import View
from .Provider import Provider


class ViewProvider(Provider):
    def __init__(self, app):
        self.application = app

    def register(self):
        view = View(self.application)
        view.add_location(self.application.make("views.location"))

        self.application.bind("view", view)

    def boot(self):
        pass

""" A View Service Provider """
from masonite.provider import ServiceProvider
from masonite.view import View


class ViewProvider(ServiceProvider):

    wsgi = False

    def register(self):
        view = View(self.app)
        self.app.bind('ViewClass', view)
        self.app.bind('View', view.render)

    def boot(self):
        pass

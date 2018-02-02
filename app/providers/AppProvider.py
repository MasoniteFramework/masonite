''' A AppProvider Service Provider '''
from masonite.provider import ServiceProvider
from masonite.request import Request
from masonite.routes import Route
from routes import web, api

class AppProvider(ServiceProvider):

    def register(self):
        self.app.bind('WebRoutes', web.ROUTES)
        self.app.bind('ApiRoutes', api.ROUTES)

    def boot(self, Environ):
        self.app.bind('Request', Request(Environ))
        self.app.bind('Route', Route(Environ))

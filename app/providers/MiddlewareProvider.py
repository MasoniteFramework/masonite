''' A MiddlewareProvider Service Provider '''
from masonite.provider import ServiceProvider
from config import middleware

class MiddlewareProvider(ServiceProvider):
    ''' Adds Middleware To The Service Container '''

    wsgi = False

    def register(self):
        ''' Register Middleware Into The Service Container '''
        self.app.bind('HttpMiddleware', middleware.HTTP_MIDDLEWARE)

    def boot(self):
        pass

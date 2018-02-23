""" A WhiteNoiseProvider Service Provider """
from masonite.provider import ServiceProvider
from whitenoise import WhiteNoise


class WhitenoiseProvider(ServiceProvider):

    wsgi = False

    def register(self):
        pass

    def boot(self, Application):
        """ Wraps the WSGI server in a whitenoise container """
        self.app.bind('WSGI', WhiteNoise(
            self.app.make('WSGI'), root=Application.STATIC_ROOT))

        for location, alias in self.app.make('Storage').STATICFILES.items():
            self.app.make('WSGI').add_files(location, prefix=alias)

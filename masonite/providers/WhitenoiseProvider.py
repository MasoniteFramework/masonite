"""A WhiteNoiseProvider Service Provider."""

from whitenoise import WhiteNoise

from masonite.provider import ServiceProvider
from config import application


class WhitenoiseProvider(ServiceProvider):

    wsgi = False

    def register(self):
        pass

    def boot(self):
        """Wrap the WSGI server in a whitenoise container."""
        self.app.bind('WSGI', WhiteNoise(
            self.app.make('WSGI'), root=self.app.make('Application').STATIC_ROOT, autorefresh=application.DEBUG))

        for location, alias in self.app.make('Storage').STATICFILES.items():
            self.app.make('WSGI').add_files(location, prefix=alias)

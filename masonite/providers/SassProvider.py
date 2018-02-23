""" A SassProvider Service Provider """
from masonite.provider import ServiceProvider
from masonite.storage import Storage


class SassProvider(ServiceProvider):

    wsgi = False 

    def register(self):
        """
        |--------------------------------------------------------------------------
        | Compile Sass
        |--------------------------------------------------------------------------
        |
        | Compile Sass if the libsass module is installed. Once installed, all
        | Sass files are compiled when the server is ran. This will only run
        | once when the server is first started.
        |
        """

        Storage().compile_sass()

    def boot(self):
        pass

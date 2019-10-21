from masonite.provider import ServiceProvider
from masonite.request import Request
from masonite.response import Response
from masonite.helpers import config


class CorsProvider(ServiceProvider):
    """Provides Services To The Service Container."""

    wsgi = True

    def register(self):
        """Register objects into the Service Container."""
        pass

    def boot(self, request: Request, response: Response):
        """Boots services required by the container."""
        headers = config('middleware.cors') or {}
        request.header(headers)

        if request.get_request_method().lower() == 'options':
            response.view('preflight')

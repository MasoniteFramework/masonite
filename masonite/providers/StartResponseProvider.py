"""A StartResponseProvider Service Provider."""

from masonite.exceptions import ResponseError
from masonite.provider import ServiceProvider
from masonite.request import Request


class StartResponseProvider(ServiceProvider):

    def register(self):
        pass

    def boot(self, request: Request):
        if not request.redirect_url:
            # Convert the data that is retrieved above to bytes
            # so the wsgi server can handle it.
            try:
                data = bytes(self.app.make('Response'), 'utf-8')
            except TypeError:
                raise ResponseError(
                    'An acceptable response type was not returned')

            self.app.bind('StatusCode', request.get_status_code())
            request.header('Content-Length', str(len(data)))
        else:
            request.status(302)
            request.header('Location', request.redirect_url)
            request.reset_redirections()
            self.app.bind('Response', 'redirecting ...')

        if self.app.has('Session') and request.get_status_code() == '200 OK':
            self.app.make('Session').reset(flash_only=True)

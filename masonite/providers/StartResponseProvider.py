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
            headers = self.app.make('Headers')
            headers += [
                ("Content-Length", str(len(data)))
            ] + request.get_cookies() + request.get_headers()
        else:
            self.app.bind('StatusCode', "302 OK")
            self.app.bind('Headers', [
                ('Location', request.redirect_url)
            ] + request.get_cookies())

            request.reset_redirections()

            self.app.bind('Response', 'redirecting ...')

        request.url_params = {}
        request.reset_headers()
        request.cookies = []
        if self.app.has('Session') and self.app.make('StatusCode') == '200 OK':
            self.app.make('Session').reset(flash_only=True)

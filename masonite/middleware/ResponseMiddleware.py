import json
from masonite.request import Request
from masonite.app import App
from masonite.exceptions import ResponseError


class ResponseMiddleware:

    def __init__(self, request: Request, app: App):
        self.request = request
        self.app = app

    def after(self):
        if not self.request.redirect_url:
            # Convert the data that is retrieved above to bytes
            # so the wsgi server can handle it.
            try:
                data = bytes(self.app.make('Response'), 'utf-8')
            except TypeError:
                raise ResponseError(
                    'An acceptable response type was not returned')

            self.app.bind('StatusCode', self.request.get_status_code())
            self.request.header('Content-Length', str(len(data)))
        else:
            self.request.status(302)
            self.request.header('Location', self.request.redirect_url)
            self.request.reset_redirections()
            self.app.bind('Response', 'redirecting ...')

        if self.app.has('Session') and self.request.get_status_code() == '200 OK':
            self.app.make('Session').reset(flash_only=True)

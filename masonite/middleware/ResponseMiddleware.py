import json
from masonite.request import Request
from masonite.response import Response
from masonite.app import App
from masonite.exceptions import ResponseError


class ResponseMiddleware:

    def __init__(self, request: Request, app: App, response: Response):
        self.request = request
        self.app = app
        self.response = response

    def after(self):
        if not self.request.redirect_url:
            # Convert the data that is retrieved above to bytes
            # so the wsgi server can handle it.
            try:
                self.response.to_bytes()
            except TypeError:
                raise ResponseError(
                    'An acceptable response type was not returned')
        else:
            self.response.redirect(self.request.redirect_url, status=302)
            self.request.reset_redirections()

        if self.app.has('Session') and self.request.get_status_code() == '200 OK':
            self.app.make('Session').reset(flash_only=True)

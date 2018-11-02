import json
from masonite.request import Request


class JsonResponseMiddleware:

    def __init__(self, request: Request):
        self.request = request

    def after(self):
        if not self.request.header('Content-Type'):
            if isinstance(self.request.app().make('Response'), dict) or isinstance(self.request.app().make('Response'), list):
                self.request.header(
                    'Content-Type', 'application/json; charset=utf-8', http_prefix=None)
                self.request.app().bind(
                    'Response',
                    str(json.dumps(self.request.app().make('Response')))
                )
            else:
                self.request.header(
                    'Content-Type', 'text/html; charset=utf-8', http_prefix=None)

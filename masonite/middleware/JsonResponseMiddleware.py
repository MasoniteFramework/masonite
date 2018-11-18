import json
from masonite.request import Request
from masonite.response import Response


class JsonResponseMiddleware:

    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response

    def after(self):
        if not self.request.header('Content-Type'):
            if isinstance(self.response.data(), dict) or isinstance(self.response.data(), list):
                self.response.json(self.response.data())
            else:
                self.request.header(
                    'Content-Type', 'text/html; charset=utf-8', http_prefix=None)

import json

from masonite.app import App
from masonite.exceptions import ResponseError
from masonite.request import Request
from masonite.response import Response


class ResponseMiddleware:

    def __init__(self, request: Request, app: App, response: Response):
        self.request = request
        self.app = app
        self.response = response

    def after(self):
        if self.request.redirect_url:
            self.response.redirect(self.request.redirect_url, status=302)
            self.request.reset_redirections()

        if self.app.has('Session') and self.request.is_status(200):
            self.app.make('Session').driver('memory').reset(flash_only=True)

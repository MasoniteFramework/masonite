import json
from masonite.exceptions import ResponseError
from masonite.view import View


class Response:

    def __init__(self, app):
        self.app = app
        self.request = self.app.make('Request')

    def json(self, payload):
        self.app.bind('Response', json.dumps(payload))
        self.request.header('Content-Length', str(len(self.app.make('Response'))))
        self.request.header('Content-Type', 'application/json; charset=utf-8')
        self.request.status(200)

        return self.data()

    def data(self):
        if self.app.has('Response'):
            return self.app.make('Response')

        return ''

    def view(self, view, status=200):
        self.request.status(status)

        if isinstance(view, View):
            view = view.rendered_template

        self.app.bind('Response', view)
        self.request.header('Content-Length', str(len(view)))

        return self.data()

    def redirect(self, location=None, status=302):
        self.request.status(status)
        if not location:
            location = self.request.redirect_url

        self.request.header('Location', location)
        self.app.bind('Response', 'redirecting ...')

        return self.data()

    def to_bytes(self):
        return bytes(self.app.make('Response'), 'utf-8')

import json
from masonite.exceptions import ResponseError
from masonite.view import View
from masonite.helpers.Extendable import Extendable


class Response(Extendable):

    def __init__(self, app):
        self.app = app
        self.request = self.app.make('Request')

    def json(self, payload):
        self.app.bind('Response', json.dumps(payload))
        self.make_headers(content_type="application/json; charset=utf-8")
        self.request.status(200)

        return self.data()

    def make_headers(self, content_type="text/html; charset=utf-8"):
        self.request.header('Content-Length', str(len(self.data())))

        self.request.header('Content-Type', content_type)

    def data(self):
        if self.app.has('Response'):
            return self.app.make('Response')

        return ''

    def converted_data(self):
        if isinstance(self.data(), dict) or isinstance(self.data(), list):
            return json.dumps(self.data())
        else:
            return self.data()

    def view(self, view, status=200):
        self.request.status(status)

        if isinstance(view, dict) or isinstance(view, list):
            return self.json(view)
        elif isinstance(view, View):
            view = view.rendered_template
        elif isinstance(view, self.request.__class__):
            view = self.data()
        elif view is None:
            raise ResponseError('Responses cannot be of type: None.')

        self.app.bind('Response', view)

        self.make_headers()

        return self.data()

    def redirect(self, location=None, status=302):
        self.request.status(status)
        if not location:
            location = self.request.redirect_url

        self.request.header('Location', location)
        self.app.bind('Response', 'redirecting ...')

        return self.data()

    def to_bytes(self):
        return bytes(self.converted_data(), 'utf-8')

"""The Masonite Response Object."""

import json

from masonite.exceptions import ResponseError
from masonite.helpers.Extendable import Extendable
from masonite.view import View

from orator.support.collection import Collection
from orator import Model
from masonite.app import App


class Response(Extendable):

    def __init__(self, app: App):
        """A Response object to be used to abstract the logic of getting a response ready to be returned.

        Arguments:
            app {masonite.app.App} -- The Masonite container.
        """
        self.app = app
        self.request = self.app.make('Request')

    def json(self, payload, status=200):
        """Gets the response ready for a JSON response.

        Arguments:
            payload {dict|list} -- Either a dictionary or a list.

        Returns:
            string -- Returns a string representation of the data
        """
        self.app.bind('Response', json.dumps(payload))
        self.make_headers(content_type="application/json; charset=utf-8")
        self.request.status(status)

        return self.data()

    def make_headers(self, content_type="text/html; charset=utf-8"):
        """Make the appropriate headers based on changes made in controllers or middleware.

        Keyword Arguments:
            content_type {str} -- The content type to set. (default: {"text/html; charset=utf-8"})
        """
        self.request.header('Content-Length', str(len(self.to_bytes())))

        # If the user did not change it directly
        if not self.request.has_raw_header('Content-Type'):
            self.request.header('Content-Type', content_type)

    def data(self):
        """Get the data that will be returned to the WSGI server.

        Returns:
            string -- Returns a string representation of the response
        """
        if self.app.has('Response'):
            return self.app.make('Response')

        return ''

    def converted_data(self):
        """Converts the data appropriately so the WSGI server can handle it.

        Returns:
            string -- Returns a string representation of the data
        """
        if isinstance(self.data(), dict) or isinstance(self.data(), list):
            return json.dumps(self.data())
        else:
            return self.data()

    def view(self, view, status=200):
        """Set a string or view to be returned.

        Arguments:
            view {string|dict|list|masonite.view.View} -- Some data type that is an appropriate response.

        Keyword Arguments:
            status {int} -- The Response status code. (default: {200})

        Raises:
            ResponseError -- If a data type that is not an acceptable response type is returned.

        Returns:
            string|dict|list -- Returns the data to be returned.
        """
        if not self.request.get_status():
            self.request.status(status)

        if isinstance(view, dict) or isinstance(view, list):
            return self.json(view, status=self.request.get_status())
        elif isinstance(view, Collection) or isinstance(view, Model):
            return self.json(view.serialize(), status=self.request.get_status())
        elif isinstance(view, int):
            view = str(view)
        elif isinstance(view, View):
            view = view.rendered_template
        elif isinstance(view, self.request.__class__):
            view = self.data()
        elif view is None:
            raise ResponseError('Responses cannot be of type: None.')

        if not isinstance(view, str):
            raise ResponseError('Invalid response type of {}'.format(type(view)))

        self.app.bind('Response', view)

        self.make_headers()

        return self.data()

    def redirect(self, location=None, status=302):
        """Set the redirection on the server.

        Keyword Arguments:
            location {string} -- The URL to redirect to (default: {None})
            status {int} -- The Response status code. (default: {302})

        Returns:
            string -- Returns the data to be returned.
        """
        self.request.status(status)
        if not location:
            location = self.request.redirect_url

        self.request.reset_headers()
        self.request.header('Location', location)
        self.app.bind('Response', 'redirecting ...')

        return self.data()

    def to_bytes(self):
        """Converts the data to bytes so the WSGI server can handle it.

        Returns:
            bytes -- The converted response to bytes.
        """
        return bytes(self.converted_data(), 'utf-8')

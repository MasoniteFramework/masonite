"""The Masonite Response Object."""

import json
import mimetypes
from pathlib import Path

from orator import LengthAwarePaginator, Model, Paginator
from orator.support.collection import Collection

from .app import App
from .exceptions import ResponseError
from .helpers.Extendable import Extendable


class Response(Extendable):
    """A Response object to be used to abstract the logic of getting a response ready to be returned.

    Arguments:
        app {masonite.app.App} -- The Masonite container.
    """

    def __init__(self, app: App):
        self.app = app
        self.request = self.app.make('Request')

    def json(self, payload, status=200):
        """Gets the response ready for a JSON response.

        Arguments:
            payload {dict|list} -- Either a dictionary or a list.

        Returns:
            string -- Returns a string representation of the data
        """
        self.app.bind('Response', bytes(json.dumps(payload), 'utf-8'))
        self.make_headers(content_type="application/json; charset=utf-8")
        self.request.status(status)

        return self.data()

    def paginated_json(self, paginator, status=200):
        """Determine type of paginated instance and return JSON response.

        Arguments:
            paginator {Paginator|LengthAwarePaginator} --
                Either an Orator Paginator or LengthAwarePaginator object

        Returns:
            string -- Returns a string representation of the data
        """
        # configured param types
        page_size_parameter = 'page_size'
        page_parameter = 'page'

        # try to capture request input for page_size and/or page
        page_size_input = self.request.input(page_size_parameter)
        page_input = self.request.input(page_parameter)
        try:
            page_size = (
                int(page_size_input)
                if page_size_input and int(page_size_input) > 0
                else paginator.per_page
            )
        except ValueError:
            page_size = paginator.per_page

        try:
            page = (
                int(page_input)
                if page_input and int(page_input) > 0
                else paginator.current_page
            )
        except ValueError:
            page = paginator.current_page

        # don't waste time instantiating new paginator if no change
        payload = {
            'total': (
                paginator.total
                if isinstance(paginator, LengthAwarePaginator)
                else None
            ),
            'count': paginator.count(),
            'per_page': page_size,
            'current_page': page,
            'last_page': (
                paginator.last_page
                if isinstance(paginator, LengthAwarePaginator)
                else None
            ),
            'from': (page_size * (page - 1)) + 1,
            'to': page_size * page,
            'data': paginator.serialize()
        }

        # remove fields not relevant to Paginator instance
        if isinstance(paginator, Paginator):
            del payload['total']
            del payload['last_page']

        return self.json(payload, status)

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
        if isinstance(self.data(), (dict, list)):
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

        if isinstance(view, tuple):
            view, status = view
            self.request.status(status)

        if not self.request.get_status():
            self.request.status(status)

        if isinstance(view, (dict, list)):
            return self.json(view, status=self.request.get_status())
        elif isinstance(view, (Collection, Model)):
            return self.json(view.serialize(), status=self.request.get_status())
        elif isinstance(view, int):
            view = str(view)
        elif isinstance(view, Responsable):
            view = view.get_response()
        elif isinstance(view, self.request.__class__):
            view = self.data()
        if isinstance(view, (Paginator, LengthAwarePaginator)):
            return self.paginated_json(view, status=self.request.get_status())
        elif view is None:
            raise ResponseError('Responses cannot be of type: None. Did you return anything in your responsable method?')

        if isinstance(view, str):
            self.app.bind('Response', bytes(view, 'utf-8'))
        else:
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
        self.view('Redirecting ...')

        return self.data()

    def to_bytes(self):
        """Converts the data to bytes so the WSGI server can handle it.

        Returns:
            bytes -- The converted response to bytes.
        """
        return self.converted_data()


class Responsable:

    def get_response(self):
        raise NotImplementedError("This class does not implement a 'get_response()' method")


class Download(Responsable):
    """Download class to help show files in the browser or force
        a download for the client browser.

    Arguments:
        location {string} -- The path you want to download.

    Keyword Arguments:
        force {bool} -- Whether you want the client's browser to force the file download (default: {False})
        name {str} -- The name you want the file to be called when downloaded (default: {'profile.jpg'})
    """

    def __init__(self, location, force=False, name='1'):
        self.location = location
        self._force = force
        self.name = name
        self.container = None

    def force(self):
        """Sets the force option.

        Returns:
            self
        """
        self._force = True
        return self

    def get_response(self):
        """Handles the way the response should be handled by the server.

        Returns:
            bytes - Returns bytes required for the server to handle the download.
        """
        if not self.container:
            from wsgi import container
            self.container = container

        request = self.container.make('Request')

        with open(self.location, 'rb') as filelike:
            data = filelike.read()

        if self._force:
            request.header('Content-Type', 'application/octet-stream')
            request.header('Content-Disposition', 'attachment; filename="{}{}"'.format(self.name, self.extension(self.location)))
        else:
            request.header('Content-Type', self.mimetype(self.location))

        return data

    def mimetype(self, path):
        """Gets the mimetime of a path

        Arguments:
            path {string} -- The path of the file to download.

        Returns:
            string -- The mimetype for use in headers
        """
        return mimetypes.guess_type(path)[0]

    def extension(self, path):
        return Path(path).suffix

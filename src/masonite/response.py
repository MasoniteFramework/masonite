"""The Masonite Response Object."""

import json
import mimetypes
from pathlib import Path

from .app import App
from .exceptions import ResponseError
from .helpers.Extendable import Extendable
from .headers import HeaderBag, Header
from .helpers.status import response_statuses
from .exceptions import InvalidHTTPStatusCode


class Response(Extendable):
    """A Response object to be used to abstract the logic of getting a response ready to be returned.

    Arguments:
        app {masonite.app.App} -- The Masonite container.
    """

    def __init__(self, app: App):
        self.app = app
        self.request = self.app.make("Request")
        self.content = ""
        self._status = None
        self.statuses = response_statuses()
        self.header_bag = HeaderBag()

    def json(self, payload, status=200):
        """Gets the response ready for a JSON response.

        Arguments:
            payload {dict|list} -- Either a dictionary or a list.

        Returns:
            string -- Returns a string representation of the data
        """
        self.content = bytes(json.dumps(payload), "utf-8")
        self.make_headers(content_type="application/json; charset=utf-8")
        self.status(status)

        return self.data()

    def make_headers(self, content_type="text/html; charset=utf-8"):
        """Make the appropriate headers based on changes made in controllers or middleware.

        Keyword Arguments:
            content_type {str} -- The content type to set. (default: {"text/html; charset=utf-8"})
        """
        self.header_bag.add(Header("Content-Length", str(len(self.to_bytes()))))

        # If the user did not change it directly
        self.header_bag.add_if_not_exists(Header("Content-Type", content_type))

    def header(self, name, value=None):
        if value is None and isinstance(name, dict):
            for name, value in name.items():
                self.header_bag.add(Header(name, value))
        elif value is None:
            return self.header_bag.get(name)

        return self.header_bag.add(Header(name, value))

    def get_and_reset_headers(self):
        header = self.header_bag
        self.header_bag = HeaderBag()
        self._status = None
        return header.render() + self.request.cookie_jar.render_response()

    def get_response_content(self):
        return self.data()

    def status(self, status):
        """Set the HTTP status code.

        Arguments:
            status {string|integer} -- A string or integer with the standardized status code

        Returns:
            self
        """
        if isinstance(status, str):
            self._status = status
        elif isinstance(status, int):
            try:
                self._status = self.statuses[status]
            except KeyError:
                raise InvalidHTTPStatusCode
        return self

    def is_status(self, code):
        return self._get_status_code_by_value(self.get_status_code()) == code

    def _get_status_code_by_value(self, value):
        for key, status in self.statuses.items():
            if status == value:
                return key

        return None

    def get_status_code(self):
        """Gets the HTTP status string like "200 OK"

        Returns:
            self
        """
        return self._status

    def get_status(self):
        return self._get_status_code_by_value(self.get_status_code())

    def data(self):
        """Get the data that will be returned to the WSGI server.

        Returns:
            string -- Returns a string representation of the response
        """
        return self.content

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
            self.status(status)

        if not self.get_status_code():
            self.status(status)

        if isinstance(view, (dict, list)):
            return self.json(view, status=self.get_status_code())
        elif hasattr(view, "serialize"):
            return self.json(view.serialize(), status=self.get_status_code())
        elif isinstance(view, int):
            view = str(view)
        elif isinstance(view, Responsable):
            view = view.get_response()
        elif isinstance(view, self.request.__class__):
            view = self.data()
        elif view is None:
            raise ResponseError(
                "Responses cannot be of type: None. Did you return anything in your responsable method?"
            )

        if isinstance(view, str):
            self.content = bytes(view, "utf-8")
            self.app.bind("Response", bytes(view, "utf-8"))
        else:
            self.content = view
            self.app.bind("Response", view)

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
        self.status(status)
        if not location:
            location = self.request.redirect_url

        self.request.reset_headers()
        self.header_bag.add(Header("Location", location))
        self.view("Redirecting ...")

        return self.data()

    def to_bytes(self):
        """Converts the data to bytes so the WSGI server can handle it.

        Returns:
            bytes -- The converted response to bytes.
        """
        return self.converted_data()


class Responsable:
    def get_response(self):
        raise NotImplementedError(
            "This class does not implement a 'get_response()' method"
        )


class Download(Responsable):
    """Download class to help show files in the browser or force
        a download for the client browser.

    Arguments:
        location {string} -- The path you want to download.

    Keyword Arguments:
        force {bool} -- Whether you want the client's browser to force the file download (default: {False})
        name {str} -- The name you want the file to be called when downloaded (default: {'profile.jpg'})
    """

    def __init__(self, location, force=False, name="1"):
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

        response = self.container.make(Response)

        with open(self.location, "rb") as filelike:
            data = filelike.read()

        if self._force:
            response.header("Content-Type", "application/octet-stream")
            response.header(
                "Content-Disposition",
                'attachment; filename="{}{}"'.format(
                    self.name, self.extension(self.location)
                ),
            )
        else:
            response.header("Content-Type", self.mimetype(self.location))

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

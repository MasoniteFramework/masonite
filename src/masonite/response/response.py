"""The Masonite Response Object."""

import json
import mimetypes
from pathlib import Path

from ..routes.Router import Router
from ..exceptions import ResponseError, InvalidHTTPStatusCode
from ..headers import HeaderBag, Header
from ..utils.http import HTTP_STATUS_CODES
from ..cookies import CookieJar


class Response:
    """A Response object to be used to abstract the logic of getting a response ready to be returned.

    Arguments:
        app {masonite.app.App} -- The Masonite container.
    """

    def __init__(self, app):
        self.app = app
        self.content = ""
        self._status = None
        self.statuses = HTTP_STATUS_CODES
        self.header_bag = HeaderBag()
        self.cookie_jar = CookieJar()
        self.original = None

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
                self.header_bag.add(Header(name, str(value)))
        elif value is None:
            header = self.header_bag.get(name)
            if isinstance(header, str):
                return header
            return header.value

        return self.header_bag.add(Header(name, value))

    def get_headers(self):
        return self.header_bag.render()

    def cookie(self, name, value=None, **options):
        if value is None:
            cookie = self.cookie_jar.get(name)
            if not cookie:
                return
            return cookie.value

        return self.cookie_jar.add(name, value, **options)

    def delete_cookie(self, name):
        self.cookie_jar.delete(name)
        return self

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
        if isinstance(self.content, str):
            return bytes(self.content, "utf-8")

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
        self.original = view

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
        elif hasattr(view, "get_response"):
            view = view.get_response()
        elif view is None:
            raise ResponseError(
                "Responses cannot be of type: None. Did you return anything in your responsable method?"
            )

        self.content = view

        self.make_headers()

        return self

    def back(self):
        return self.redirect(url=self.app.make("request").get_back_path())

    def redirect(self, location=None, name=None, params={}, url=None, status=302):
        """Set the redirection on the server.

        Keyword Arguments:
            location {string} -- The URL to redirect to (default: {None})
            status {int} -- The Response status code. (default: {302})
            params {dict} -- The route params (default: {})

        Returns:
            string -- Returns the data to be returned.
        """
        self.status(status)

        if location:
            self.header_bag.add(Header("Location", location))
        elif name:
            url = self._get_url_from_route_name(name, params)
            self.header_bag.add(Header("Location", url))
        elif url:
            self.header_bag.add(Header("Location", url))
        self.view("Redirecting ...")
        return self

    def _get_url_from_route_name(self, name, params={}):
        route = self.app.make("router").find_by_name(name)
        if not route:
            raise ValueError(f"Route with the name '{name}' not found.")
        return Router.compile_to_url(route.url, params)

    def to_bytes(self):
        """Converts the data to bytes so the WSGI server can handle it.

        Returns:
            bytes -- The converted response to bytes.
        """
        return self.converted_data()

    def download(self, name, location, force=False):
        if force:
            self.header("Content-Type", "application/octet-stream")
            self.header(
                "Content-Disposition",
                'attachment; filename="{}{}"'.format(name, self.extension(location)),
            )
        else:
            self.header("Content-Type", self.mimetype(location))

        with open(location, "rb") as filelike:
            data = filelike.read()

        return self.view(data)

    def extension(self, path):
        return Path(path).suffix

    def mimetype(self, path):
        """Gets the mimetime of a path

        Arguments:
            path {string} -- The path of the file to download.

        Returns:
            string -- The mimetype for use in headers
        """
        return mimetypes.guess_type(path)[0]

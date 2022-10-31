"""The Masonite Response Object."""

import json
import mimetypes
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..foundation import Application

from ..routes.Router import Router
from ..exceptions import ResponseError, InvalidHTTPStatusCode, RouteNotFoundException
from ..headers import HeaderBag, Header
from ..utils.http import HTTP_STATUS_CODES
from ..utils.str import add_query_params
from ..cookies import CookieJar


class Response:
    """A Response object to be used to abstract the logic of getting a response ready to be
    returned."""

    def __init__(self, app: "Application"):
        self.app = app
        self.content: str = ""
        self._status: str = None
        self.statuses: dict = HTTP_STATUS_CODES
        self.header_bag = HeaderBag()
        self.cookie_jar = CookieJar()
        self.original = None

    def json(self, payload: Any, status: int = 200) -> bytes:
        """Set the response as a JSON response."""
        self.content = bytes(json.dumps(payload, ensure_ascii=False), "utf-8")
        self.make_headers(content_type="application/json; charset=utf-8")
        self.status(status)

        return self.data()

    def make_headers(self, content_type: str = "text/html; charset=utf-8") -> None:
        """Recompute Content-Length of the response after modifying it."""
        self.header_bag.add(Header("Content-Length", str(len(self.to_bytes()))))

        # If the user did not change it directly
        self.header_bag.add_if_not_exists(Header("Content-Type", content_type))

    def header(self, name: str, value: str = None) -> "None|str":
        """Get response header for the given name if no value provided or add headers to response."""
        if value is None and isinstance(name, dict):
            for name, value in name.items():
                self.header_bag.add(Header(name, str(value)))
        elif value is None:
            header = self.header_bag.get(name)
            if isinstance(header, str):
                return header
            return header.value

        return self.header_bag.add(Header(name, value))

    def with_headers(self, headers: dict) -> "Response":
        """Add headers dictionary to response headers."""
        for name, value in headers.items():
            self.header_bag.add(Header(name, str(value)))
        return self

    def get_headers(self) -> list:
        return self.header_bag.render()

    def cookie(self, name: str, value: str = None, **options) -> "None|str":
        """Get response cookie for the given name if no value provided or add cookie to
        the response with the given name, value and options."""
        if value is None:
            cookie = self.cookie_jar.get(name)
            if not cookie:
                return
            return cookie.value

        return self.cookie_jar.add(name, value, **options)

    def delete_cookie(self, name: str) -> "Response":
        """Delete the cookie with the given name from the response."""
        self.cookie_jar.delete(name)
        return self

    def get_response_content(self) -> bytes:
        """Get response content."""
        return self.data()

    def status(self, status: "str|int") -> "Response":
        """Set HTTP status code of the response."""
        if isinstance(status, str):
            self._status = status
        elif isinstance(status, int):
            try:
                self._status = self.statuses[status]
            except KeyError:
                raise InvalidHTTPStatusCode
        return self

    def is_status(self, code: int) -> bool:
        """Check if response has the given status code."""
        return self._get_status_code_by_value(self.get_status_code()) == code

    def _get_status_code_by_value(self, value: int) -> "str|None":
        for key, status in self.statuses.items():
            if status == value:
                return key

        return None

    def get_status_code(self) -> str:
        """Gets the HTTP status code of the response as a human string, like "200 OK"."""
        return self._status

    def get_status(self):
        return self._get_status_code_by_value(self.get_status_code())

    def data(self) -> bytes:
        """Get the response content as bytes."""
        if isinstance(self.content, str):
            return bytes(self.content, "utf-8")

        return self.content

    def converted_data(self) -> "str|bytes":
        """Get the response content as string or bytes so that the WSGI server handles it."""
        if isinstance(self.data(), (dict, list)):
            return json.dumps(self.data(), ensure_ascii=False)
        else:
            return self.data()

    def view(self, view: Any, status: int = 200) -> "bytes|Response":
        """Set the response as a string or view."""
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

    def back(self) -> "Response":
        """Set the response as a redirect response back to previous path defined from the
        request."""
        return self.redirect(url=self.app.make("request").get_back_path())

    def redirect(
        self,
        location: str = None,
        name: str = None,
        params: dict = {},
        url: str = None,
        status: int = 302,
        query_params={},
    ) -> "Response":
        """Set the response as a redirect response. The redirection location can be defined
        with the location URL or with a route name. If a route name is used, route params can
        be provided."""

        self.status(status)

        if location:
            location = add_query_params(location, query_params)
            self.header_bag.add(Header("Location", location))
        elif name:
            url = self._get_url_from_route_name(name, params, query_params)
            self.header_bag.add(Header("Location", url))
        elif url:
            url = add_query_params(url, query_params)
            self.header_bag.add(Header("Location", url))
        self.view("Redirecting ...")
        return self

    def _get_url_from_route_name(
        self, name: str, params: dict = {}, query_params: dict = {}
    ) -> str:
        route = self.app.make("router").find_by_name(name)
        if not route:
            raise RouteNotFoundException(f"Could not find route with the name '{name}'")
        return Router.compile_to_url(route.url, params, query_params)

    def to_bytes(self) -> "bytes":
        """Converts the response to bytes."""
        return self.converted_data()

    def download(self, name: str, location: str, force: bool = False) -> "Response":
        """Set the response as a file download response."""
        if force:
            self.header("Content-Type", "application/octet-stream")
            self.header(
                "Content-Disposition",
                'attachment; filename="{}{}"'.format(name, Path(location).suffix),
            )
        else:
            self.header("Content-Type", mimetypes.guess_type(location)[0])

        with open(location, "rb") as filelike:
            data = filelike.read()

        return self.view(data)

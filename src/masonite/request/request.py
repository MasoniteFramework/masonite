import re
import tldextract
from typing import TYPE_CHECKING, Any

from ..cookies import CookieJar
from ..headers import HeaderBag, Header
from ..input import InputBag
from .validation import ValidatesRequest
from ..authorization import AuthorizesRequest
from ..sessions import old as old_helper

if TYPE_CHECKING:
    from ..routes import Route


class Request(ValidatesRequest, AuthorizesRequest):
    def __init__(self, environ: dict):
        """Initializes a request with the WSGI environment dictionary."""
        self.environ = environ
        self.cookie_jar = CookieJar()
        self.header_bag = HeaderBag()
        self.input_bag = InputBag()
        self._ip = None
        self.params = {}
        self._user = None
        self.route = None
        self._subdomains_activated = False
        self.load()

    def load(self):
        """Load request from environment."""
        self.cookie_jar.load(self.environ.get("HTTP_COOKIE", ""))
        self.header_bag.load(self.environ)
        self.input_bag.load(self.environ)

    def load_params(self, params: dict = None):
        """Load request parameters."""
        if not params:
            params = {}

        self.params.update(params)

    def param(self, param: str, default: str = "") -> str:
        """Get query string parameter from request."""
        return self.params.get(param, default)

    def get_route(self) -> "Route":
        """Get Route associated to request if any."""
        return self.route

    def get_path(self) -> str:
        """Get request path (read from PATH_INFO) environment variable without eventual query
        string parameters."""
        return self.environ.get("PATH_INFO")

    def get_path_with_query(self) -> str:
        """Get request path (read from PATH_INFO) environment variable with eventual query
        string parameters."""
        query_string = self.environ.get("QUERY_STRING")
        if query_string:
            return self.get_path() + "?" + query_string
        else:
            return self.get_path()

    def get_back_path(self) -> str:
        """Get previous request path if it has been defined as '__back' input."""
        return self.input("__back") or self.get_path_with_query()

    def get_request_method(self) -> str:
        """Get request method (read from REQUEST_METHOD environment variable)."""
        return self.input("__method") or self.environ.get("REQUEST_METHOD")

    def input(self, name: str, default: str = "") -> str:
        """Get a specific request input value with the given name. If the value does not exist in
        the request return the default value."""
        name = str(name)

        return self.input_bag.get(name, default=default)

    def cookie(self, name: str, value: str = None, **options) -> None:
        """If no value provided, read the cookie value with the given name from the request. Else
        create a cookie in the request with the given name and value.
        Some options can be passed when creating cookie, refer to CookieJar class."""
        if value is None:
            cookie = self.cookie_jar.get(name)
            if not cookie:
                return
            return cookie.value

        return self.cookie_jar.add(name, value, **options)

    def delete_cookie(self, name: str) -> "Request":
        """Delete cookie with the given name from the request."""
        self.cookie_jar.delete(name)
        return self

    def header(self, name: str, value: str = None) -> "str|None":
        """If no value provided, read the header value with the given name from the request. Else
        add a header in the request with the given name and value."""
        if value is None:
            header = self.header_bag.get(name)
            if not header:
                return
            return header.value
        else:
            return self.header_bag.add(Header(name, value))

    def all(self) -> dict:
        """Get all inputs from the request as a dictionary."""
        return self.input_bag.all_as_values()

    def only(self, *inputs: str) -> dict:
        """Pass arguments as string arguments such as request.only("arg1", "arg2") to get back a dictionary of only those inputs."""
        return self.input_bag.only(*inputs)

    def old(self, key: str):
        """Get value from session for the given key."""
        return old_helper(key)

    def is_not_safe(self) -> bool:
        """Check if the current request is considered 'safe', meaning that the request method is
        GET, OPTIONS or HEAD."""
        if not self.get_request_method() in ("GET", "OPTIONS", "HEAD"):
            return True

        return False

    def is_ajax(self) -> bool:
        """Check if the current request is an AJAX request."""
        return self.header("X-Requested-With") == "XMLHttpRequest"

    def user(self) -> "None|Any":
        """Get the current authenticated user if any. LoadUserMiddleware needs to be used for user
        to be populated in request."""
        return self._user

    def set_user(self, user: Any) -> "Request":
        """Set the current authenticated user of the request."""
        self._user = user
        return self

    def remove_user(self) -> "Request":
        """Log out user of the current request."""
        self._user = None
        return self

    def contains(self, route: str) -> bool:
        """Check if current request path match the given URL."""
        if not route.startswith("/"):
            route = "/" + route

        regex = re.compile(route.replace("*", "[a-zA-Z0-9_]+"))

        return regex.match(self.get_path())

    def get_subdomain(self, exclude_www: bool = True) -> "None|str":
        """Get the request subdomain if subdomains are enabled."""
        if not self._subdomains_activated:
            return None

        url = tldextract.extract(self.get_host())
        if url.subdomain == "" or (
            url.subdomain and exclude_www and url.subdomain == "www"
        ):
            return None

        return url.subdomain

    def get_host(self) -> str:
        """Get the request host (from HTTP_HOST environment variable)."""
        return self.environ.get("HTTP_HOST")

    def activate_subdomains(self):
        """Enable subdomains for this request."""
        self._subdomains_activated = True
        return self

    def ip(self) -> "str|None":
        """Return the request IP by processing the different headers setup in IpMiddleware."""
        return self._ip

    def accepts_json(self) -> bool:
        """Check if request Accept header contains application/json."""
        return "application/json" in str(self.header("Accept"))

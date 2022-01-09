from ..cookies import CookieJar
from ..headers import HeaderBag, Header
from ..input import InputBag
import re
import tldextract
from .validation import ValidatesRequest
from ..authorization import AuthorizesRequest


class Request(ValidatesRequest, AuthorizesRequest):
    def __init__(self, environ):
        """Request class constructor.

        Initializes several properties and sets various methods
        depending on the environtment.

        Keyword Arguments:
            environ {dictionary} -- WSGI environ dictionary. (default: {None})
        """
        self.environ = environ
        self.cookie_jar = CookieJar()
        self.header_bag = HeaderBag()
        self.input_bag = InputBag()
        self.params = {}
        self._user = None
        self.load()

    def load(self):
        self.cookie_jar.load(self.environ.get("HTTP_COOKIE", ""))
        self.header_bag.load(self.environ)
        self.input_bag.load(self.environ)

    def load_params(self, params=None):
        if not params:
            params = {}

        self.params.update(params)

    def param(self, param, default=""):
        return self.params.get(param, default)

    def get_path(self):
        return self.environ.get("PATH_INFO")

    def get_path_with_query(self):
        return self.environ.get("PATH_INFO") + "?" + self.environ.get("QUERY_STRING")

    def get_back_path(self):
        return self.input("__back") or self.get_path_with_query()

    def get_request_method(self):
        return self.environ.get("REQUEST_METHOD")

    def input(self, name, default=""):
        """Get a specific input value.

        Arguments:
            name {string} -- Key of the input data

        Keyword Arguments:
            default {string} -- Default value if input does not exist (default: {False})
            clean {bool} -- Whether or not the return value should be
                            cleaned (default: {True})

        Returns:
            string
        """
        name = str(name)

        return self.input_bag.get(name, default=default)

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

    def header(self, name, value=None):
        if value is None:
            header = self.header_bag.get(name)
            if not header:
                return
            return header.value
        else:
            return self.header_bag.add(Header(name, value))

    def all(self):
        return self.input_bag.all_as_values()

    def only(self, *inputs):
        return self.input_bag.only(*inputs)

    def is_not_safe(self):
        """Check if the current request is not a get request.

        Returns:
            bool
        """
        if not self.get_request_method() in ("GET", "OPTIONS", "HEAD"):
            return True

        return False

    def user(self):
        return self._user

    def set_user(self, user):
        self._user = user
        return self

    def remove_user(self):
        self._user = None
        return self

    def contains(self, route):
        if not route.startswith("/"):
            route = "/" + route

        regex = re.compile(route.replace("*", "[a-zA-Z0-9_]+"))

        return regex.match(self.get_path())

    def get_subdomain(self, exclude_www=True):
        url = tldextract.extract(self.get_host())
        if url.subdomain == "" or (
            url.subdomain and exclude_www and url.subdomain == "www"
        ):
            return None

        return url.subdomain

    def get_host(self):
        return self.environ.get("HTTP_HOST")

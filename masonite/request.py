"""Request Module.

Request Module handles many different aspects of a single request
Methods which require the request and help ease development should
be put here.

Methods may return another object if necessary to expand capabilities
of this class.
"""

import re
from cgi import MiniFieldStorage
from http import cookies
from urllib.parse import parse_qsl

import tldextract
from cryptography.fernet import InvalidToken

from config import application
from masonite.auth.Sign import Sign
from masonite.exceptions import InvalidHTTPStatusCode, RouteException
from masonite.helpers import dot, clean_request_input, Dot as DictDot
from masonite.helpers.Extendable import Extendable
from masonite.helpers.routes import compile_route_to_regex
from masonite.helpers.status import response_statuses
from masonite.helpers.time import cookie_expire_time


class Request(Extendable):
    """Handles many different aspects of a single request.

    This is the object passed through to the controllers
    as a request parameter

    Arguments:
        Extendable {masonite.helpers.Extendable.Extendable} -- Makes this class have the ability to extend another class at runtime.
    """

    statuses = response_statuses()

    def __init__(self, environ=None):
        """Request class constructor.

        Initializes several properties and sets various methods
        depending on the environtment.

        Keyword Arguments:
            environ {dictionary} -- WSGI environ dictionary. (default: {None})
        """
        self.cookies = []
        self._headers = {}
        self.url_params = {}
        self.redirect_url = False
        self.redirect_route = False
        self.user_model = None
        self.subdomain = None
        self._activate_subdomains = False
        self._status = None

        if environ:
            self.load_environ(environ)

        self.encryption_key = False
        self.container = None

    def input(self, name, default=False, clean=True):
        """Get a specific input value.

        Arguments:
            name {string} -- Key of the input data

        Keyword Arguments:
            default {string} -- Default value if input does not exist (default: {False})
            clean {bool} -- Whether or not the return value should be cleaned (default: {True})

        Returns:
            string
        """
        if '.' in name and isinstance(self.request_variables.get(name.split('.')[0]), dict):
            value = DictDot().dot(name, self.request_variables)
            if value:
                return value

        elif '.' in name:
            name = dot(name, "{1}[{.}]")

        return clean_request_input(self.request_variables.get(name, default), clean=clean)

    def is_post(self):
        """Check if the current request is a POST request.

        Returns:
            bool
        """
        if self.environ['REQUEST_METHOD'] == 'POST':
            return True

        return False

    def is_not_get_request(self):
        """Check if the current request is not a get request.

        Returns:
            bool
        """
        if not self.environ['REQUEST_METHOD'] == 'GET':
            return True

        return False

    def __set_request_method(self):
        """Private method for manually setting the request method.

        Returns:
            bool
        """
        if self.has('__method'):
            self.environ['REQUEST_METHOD'] = self.input('__method')
            return True

        return False

    def key(self, key):
        """Set the encryption key.

        Arguments:
            key {string} -- Encryption key

        Returns:
            self
        """
        self.encryption_key = key
        return self

    def all(self, internal_variables=True, clean=True):
        """Get all the input data.

        Keyword Arguments:
            internal_variables {bool} -- Get the internal framework variables as well (default: {True})
            clean {bool} -- Whether or not the return value should be cleaned (default: {True})

        Returns:
            dict
        """
        if not internal_variables:
            without_internals = {}
            for key, value in self.request_variables.items():
                if not key.startswith('__'):
                    without_internals.update({key: value})
            return clean_request_input(without_internals, clean=clean)

        return clean_request_input(self.request_variables, clean=clean)

    def only(self, *names):
        """Return the specified request variables in a dictionary.

        Returns:
            dict
        """
        only_vars = {}

        for name in names:
            only_vars[name] = self.request_variables.get(name)

        return only_vars

    def without(self, *names):
        """Return the request variables in a dictionary without specified values.

        Returns:
            dict
        """
        only_vars = {}

        for name in self.request_variables.keys():
            if name not in names:
                only_vars[name] = self.request_variables.get(name)

        return only_vars

    def load_app(self, app):
        """Load the container into the request class.

        Arguments:
            app {masonite.app.App} -- Application Container

        Returns:
            self
        """
        self.container = app
        return self

    def load_environ(self, environ):
        """Load the wsgi environment and sets various properties.

        Arguments:
            environ {dict} -- WSGI environ

        Returns:
            self
        """
        self.environ = environ
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.request_variables = {}
        self._set_standardized_request_variables(environ['QUERY_STRING'])

        if self.has('__method'):
            self.__set_request_method()

        return self

    def _set_standardized_request_variables(self, variables):
        """The input data is not perfect so we have to standardize it into a dictionary.

        Arguments:
            variables {string|dict}
        """
        if isinstance(variables, str):
            variables = dict(parse_qsl(variables))

        try:
            for name in variables.keys():
                value = self._get_standardized_value(variables[name])
                self.request_variables[name.replace('[]', '')] = value
        except TypeError:
            self.request_variables = {}

    def _get_standardized_value(self, value):
        """Get the standardized value based on the type of the value parameter.

        Arguments:
            value {list|dict|cgi.FileStorage|string}

        Returns:
            string|bool
        """
        if value is None:
            return None

        if isinstance(value, list):

            # If the list contains MiniFieldStorage objects then loop through and get the values.
            if any(isinstance(storage_obj, MiniFieldStorage) for storage_obj in value):
                values = [storage_obj.value for storage_obj in value]

                # TODO: This needs to be removed in 2.2. A breaking change but
                # this code will result in inconsistent values
                # If there is only 1 element in the list then return the only value in the list
                if len(values) == 1:
                    return values[0]
                return values

            return value

        if isinstance(value, dict):
            return value

        try:
            return int(value)
        except (ValueError, TypeError):
            pass

        if isinstance(value, str):
            return value

        if not value.filename:
            return value.value

        if value.filename:
            return value

        return False

    def app(self):
        """Return the application container.

        Returns:
            masonite.app.App -- Application container
        """
        return self.container

    def has(self, *args):
        """Check if all given keys in request variable exists.

        Returns:
            bool
        """
        return all((arg in self.request_variables) for arg in args)

    def status(self, status):
        """Set the HTTP status code.

        Arguments:
            status {string|integer} -- A string or integer with the standardized status code

        Returns:
            self
        """
        if isinstance(status, str):
            self.app().bind('StatusCode', status)
        elif isinstance(status, int):
            try:
                text_status = self.statuses[status]
            except KeyError:
                raise InvalidHTTPStatusCode
            self.app().bind('StatusCode', text_status)
        return self

    def get_status_code(self):
        """Return the current request status code.

        Returns:
            string -- Returns the status code (404 Not Found, 200 OK, etc)
        """
        return self.app().make('StatusCode')

    def is_status(self, code):
        return self._get_status_code_by_value(self.get_status_code()) == code

    def route_exists(self, url):
        web_routes = self.container.make('WebRoutes')

        for route in web_routes:
            if route.route_url == url:
                return True

        return False

    def _get_status_code_by_value(self, value):
        for key, status in self.statuses.items():
            if status == value:
                return key

        return None

    def get_status(self):
        return self._get_status_code_by_value(self.get_status_code())

    def get_request_method(self):
        """Get the current request method.

        Returns:
            string -- returns GET, POST, PUT, etc
        """
        return self.environ['REQUEST_METHOD']

    def header(self, key, value=None, http_prefix=None):
        """Set or gets a header depending on if "value" is passed in or not.

        Arguments:
            key {string|dict} -- The header you want to set or get. If the key is a dictionary, loop through each key pair
                                    and add them to the headers.

        Keyword Arguments:
            value {string} -- The value you want to set (default: {None})
            http_prefix {bool} -- Whether it should have `HTTP_` prefixed to the value being set. (default: {True})

        Returns:
            string|None|True -- Either return the value if getting a header, None if it doesn't exist or True if setting the headers.
        """
        if isinstance(key, dict):
            for key, value in key.items():
                self._set_header(key, value, http_prefix)
            return True

        # Get Headers
        if value is None:
            if key in self.environ:
                return self.environ[key]
            else:
                return ''

        self._set_header(key, value, http_prefix)

        return True

    def _set_header(self, key, value, http_prefix):
        # Set Headers
        if http_prefix:
            self.environ['HTTP_{0}'.format(key)] = str(value)
            self._headers.update({'HTTP_{0}'.format(key): str(value)})
        else:
            self.environ[key] = str(value)
            self._headers.update({key: str(value)})

    def get_headers(self):
        """Return all current headers to be set.

        Returns:
            list -- List containing a tuple of headers.
        """

        return self._compile_headers_to_tuple() + self.get_cookies()

    def _compile_headers_to_tuple(self):
        """Compiles the current headers to a list of tuples.

        Returns:
            list -- A list of tuples.
        """

        headers = []
        for key, value in self._headers.items():
            headers.append((key, value))

        return headers

    def reset_headers(self):
        """Reset all headers being set.

        Typically ran at the end of the request
        because of this object acts like a singleton.

        Returns:
            None
        """
        self._headers = {}

    def get_and_reset_headers(self):
        """Gets the headers but resets at the same time.

        This is useful at the end of the WSGI request to prevent
        Several requests from

        Returns:
            tuple
        """
        headers = self.get_headers()
        self.reset_headers()
        self.url_params = {}
        self.cookies = []
        return headers

    def set_params(self, params):
        """Load the params into the class.

        These parameters are where the developer can retrieve the
        /url/@variable:string/ from the url.

        Arguments:
            params {dict} -- Dictionary of parameters to store on the class.

        Returns:
            self
        """
        self.url_params.update(params)
        return self

    def param(self, parameter):
        """Retrieve the param from the URL.

        The "parameter" parameter in this method should be the name of the
        @variable passed into the url in web.py.

        Arguments:
            parameter {string} -- Specific argument to return.

        Returns:
            string|False -- Returns False if key does not exist.
        """
        if parameter in self.url_params:
            return self.url_params[parameter]
        return False

    def cookie(self, key, value, encrypt=True,
               http_only="HttpOnly;", path='/', expires=''):
        """Set a cookie in the browser.

        Arguments:
            key {string} -- Name of the cookie you want set.
            value {string} -- Value of the cookie you want set.

        Keyword Arguments:
            encrypt {bool} -- Whether or not you want to encrypt the cookie (default: {True})
            http_only {str} -- If the cookie is HttpOnly or not (default: {"HttpOnly;"})
            path {str} -- The path of the cookie to be set to. (default: {'/'})
            expires {string} -- When the cookie expires (5 minutes, 1 minute, 10 hours, etc) (default: {''})

        Returns:
            self
        """
        if encrypt:
            value = Sign(self.encryption_key).sign(value)
        else:
            value = value

        if expires:
            expires = "Expires={0};".format(cookie_expire_time(expires))

        if not http_only:
            http_only = ""

        self.append_cookie(key, '{0}={1};{2} {3}Path={4}'.format(key, value, expires, http_only, path))
        self.cookies.append(
            ('Set-Cookie', '{0}={1};{2} {3}Path={4}'.format(
                key, value, expires, http_only, path)))
        return self

    def get_cookies(self):
        """Retrieve all cookies from the browser.

        Returns:
            dict -- Returns all the cookies.
        """
        return self.cookies

    def get_raw_cookie(self, provided_cookie):
        if 'HTTP_COOKIE' in self.environ:
            grab_cookie = cookies.SimpleCookie(self.environ['HTTP_COOKIE'])
            if provided_cookie in grab_cookie:
                return grab_cookie[provided_cookie]

        return None

    def get_cookie(self, provided_cookie, decrypt=True):
        """Retrieve a specific cookie from the browser.

        Arguments:
            provided_cookie {string} -- Name of the cookie to retrieve

        Keyword Arguments:
            decrypt {bool} -- Whether Masonite should try to decrypt the cookie.
                              This should only be True if the cookie was encrypted
                              in the first place.  (default: {True})

        Returns:
            string|None -- Returns None if the cookie does not exist.
        """
        if 'HTTP_COOKIE' in self.environ:
            grab_cookie = cookies.SimpleCookie(self.environ['HTTP_COOKIE'])

            if provided_cookie in grab_cookie:
                if decrypt:
                    try:
                        return Sign(self.encryption_key).unsign(
                            grab_cookie[provided_cookie].value)
                    except InvalidToken:
                        self.delete_cookie(provided_cookie)
                        return None

                return grab_cookie[provided_cookie].value
        return None

    def append_cookie(self, key, value):
        """Append cookie to the string or create a new string.

        Whether a new cookie should append on to the string of cookies to be set
        or create a new string. This string is used by the browser to interpret how
        handle setting a cookie.

        Arguments:
            key {string} -- Name of cookie to be stored
            value {string} -- Value of cookie to be stored
        """
        if 'HTTP_COOKIE' in self.environ and self.environ['HTTP_COOKIE']:
            self.environ['HTTP_COOKIE'] += ';{}'.format(value)
        else:
            self.environ['HTTP_COOKIE'] = '{}'.format(value)

    def delete_cookie(self, key):
        """Delete cookie.

        Arguments:
            key {string} -- Name of cookie to be deleted.

        Returns:
            bool -- Whether or not the cookie was successfully deleted.
        """
        for index, cookie in enumerate(self.cookies):
            if cookie[1].startswith(key + '='):
                del self.cookies[index]

        self.cookie(key, '', expires='expired')

        if 'HTTP_COOKIE' in self.environ and self.environ['HTTP_COOKIE']:

            cookies = self.environ['HTTP_COOKIE'].split(';')
            for index, cookie in enumerate(cookies):
                if cookie.startswith(key):
                    # remove that cookie
                    del cookies[index]

            # put string back together
            self.environ['HTTP_COOKIE'] = ';'.join(cookies)
            return True
        return False

    def set_user(self, user_model):
        """Load the user into the class.

        Arguments:
            user_model {app.User.User} -- Defaults to loading this class unless specifically changed.

        Returns:
            self
        """
        self.user_model = user_model
        return self

    def user(self):
        """Load the user into the class.

        Returns:
            app.User.User|None -- Returns None if the user is not loaded or logged in.
        """
        return self.user_model

    def redirect(self, route=None, params={}, name=None, controller=None, status=302):
        """Redirect the user based on the route specified.

        Arguments:
            route {string} -- URI of the route (/dashboard/user)

        Keyword Arguments:
            params {dict} -- Dictionary of parameters to set for the URI.
                             Use this when the URI has something like
                             /dashboard/user/@id. (default: {{}})

        Returns:
            self
        """
        if name:
            return self.redirect_to(name, params, status=status)
        elif route:
            self.redirect_url = self.compile_route_to_url(route, params)
        elif controller:
            self.redirect_url = self.url_from_controller(controller, params)

        self.status(status)
        return self

    def redirect_to(self, route_name, params={}, status=302):
        """Redirect to a named route.

        Arguments:
            route_name {string} -- Name of a named route.

        Keyword Arguments:
            params {dict} -- Dictionary of parameters to set for the URI.
                             Use this when the URI has something like
                             /dashboard/user/@id. (default: {{}})

        Returns:
            self
        """
        self.redirect_url = self._get_named_route(route_name, params)
        self.status(status)

        return self

    def _get_named_route(self, name, params):
        """Search the list of routes and returns the route with the name passed.

        Arguments:
            name {string} -- Route name to search for (dashboard.user).
            params {dict} -- Dictionary of items to pass to the named route.

        Returns:
            string|None -- Returns None if the route was not found or returns the
                           compiled URI.
        """
        web_routes = self.container.make('WebRoutes')

        for route in web_routes:
            if route.named_route == name:
                return self.compile_route_to_url(route.route_url, params)

        return None

    def _get_route_from_controller(self, controller):
        """Get the route using the controller.

        This finds the route with the attached controller and returns that route.
        This does not compile the URI but actually returns the Route object.

        Arguments:
            controller {string|object} -- Can pass in either a string controller
                                          or the controller itself (the object)

        Returns:
            masonite.routes.Route|None -- Returns None if the route could not be found.
        """
        web_routes = self.container.make('WebRoutes')

        if not isinstance(controller, str):
            module_location = controller.__module__
            controller = controller.__qualname__.split('.')
        else:
            module_location = 'app.http.controllers'
            controller = controller.split('@')

        for route in web_routes:
            if route.controller.__name__ == controller[0] and route.controller_method == controller[1] and route.module_location == module_location:
                return route

    def url_from_controller(self, controller, params={}):
        """Return the compiled URI using a controller.

        Arguments:
            controller {string|object} -- Can be a string controller or a controller object.

        Keyword Arguments:
            params {dict} -- Dictionary of parameters to pass to the route for compilation. (default: {{}})

        Returns:
            masonite.routes.Route|None -- Returns None if the route could not be found.
        """
        return self.compile_route_to_url(self._get_route_from_controller(controller).route_url, params)

    def route(self, name, params={}, full=False):
        """Get a route URI by its name.

        Arguments:
            name {string} -- Name of the route.

        Keyword Arguments:
            params {dict} -- Dictionary of parameters to pass to the route for compilation. (default: {{}})
            full {bool} -- Specifies whether the full application url should be returned or not. (default: {False})

        Returns:
            masonite.routes.Route|None -- Returns None if the route cannot be found.
        """
        if full:
            route = application.URL + self._get_named_route(name, params)
        else:
            try:
                route = self._get_named_route(name, params)
            except KeyError:
                params.update(self.url_params)
                route = self._get_named_route(name, params)

        if not route:
            raise RouteException("Route with the name of '{}' was not found.".format(name))

        return route

    def reset_redirections(self):
        """Reset the redirections because of this class acting like a singleton pattern."""
        self.redirect_url = False
        self.redirect_route = False

    def back(self, default=None):
        """Return a URI for redirection depending on several use cases.

        Keyword Arguments:
            default {string} -- Default value if nothing can be found. (default: {None})

        Returns:
            self
        """
        redirect_url = self.input('__back')
        if not redirect_url and default:
            return self.redirect(default)
        elif not redirect_url and not default:
            return self.redirect(self.path)  # Some global default?

        return self.redirect(redirect_url)

    def is_named_route(self, name, params={}):
        """Check if the current URI is a specific named route.

        Arguments:
            name {string} -- The name of a route.

        Keyword Arguments:
            params {dict} -- Dictionary of parameters to pass to the route. (default: {{}})

        Returns:
            bool
        """
        if self._get_named_route(name, params) == self.path:
            return True

        return False

    def contains(self, route):
        """If the specified URI is in the current URI path.

        Arguments:
            route {string} -- Part of a URI (/dashboard)

        Returns:
            bool
        """
        return re.match(compile_route_to_regex(route), self.path)

    def compile_route_to_url(self, route, params={}):
        """Compile the route url into a usable url.

        Converts /url/@id into /url/1. Used for redirection

        Arguments:
            route {string} -- An uncompiled route (/dashboard/@user:string/@id:int)

        Keyword Arguments:
            params {dict} -- Dictionary of parameters to pass to the route (default: {{}})

        Returns:
            string -- Returns a compiled string (/dashboard/joseph/1)
        """
        if "http" in route:
            return route

        # Split the url into a list
        split_url = route.split('/')

        # Start beginning of the new compiled url
        compiled_url = '/'

        # Iterate over the list
        for url in split_url:
            if url:
                # if the url contains a parameter variable like @id:int
                if '@' in url:
                    url = url.replace('@', '').split(':')[0]
                    if isinstance(params, dict):
                        compiled_url += str(params[url]) + '/'
                    elif isinstance(params, list):
                        compiled_url += str(params[0]) + '/'
                        del params[0]
                else:
                    compiled_url += url + '/'

        # The loop isn't perfect and may have an unwanted trailing slash
        if compiled_url.endswith('/') and not route.endswith('/'):
            compiled_url = compiled_url[:-1]

        # The loop isn't perfect and may have 2 slashes next to eachother
        if '//' in compiled_url:
            compiled_url = compiled_url.replace('//', '/')

        return compiled_url

    def activate_subdomains(self):
        """Activate subdomains abilities."""
        self._activate_subdomains = True

    def has_subdomain(self):
        """Check if the current URI has a subdomain.

        Returns:
            bool
        """
        if self._activate_subdomains:
            url = tldextract.extract(self.environ['HTTP_HOST'])

            if url.subdomain:
                self.subdomain = url.subdomain
                self.url_params.update({'subdomain': self.subdomain})
                return True

        return False

    def send(self, params):
        """DEPRECATED :: sets a dictionary to be compiled for a route.

        Arguments:
            params {dict} -- Dictionary of parameters you want to pass to the route.

        Returns:
            self
        """
        self.set_params(params)
        return self

    def helper(self):
        """Dummy method to work with returning the class. Used for helper methods in the View class.

        Returns:
            self
        """
        return self

    def pop(self, *input_variables):
        """Delete keys from the request input."""
        for key in input_variables:
            if key in self.request_variables:
                del self.request_variables[key]

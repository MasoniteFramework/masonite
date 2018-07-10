"""
Request Module handles many different aspects of a single request
Methods which require the request and help ease development should
be put here.

Methods may return another object if necessary to expand capabilities
of this class.
"""
from urllib.parse import parse_qs
import re
from masonite.helpers.routes import compile_route_to_regex
from http import cookies

import tldextract

from masonite.auth.Sign import Sign
from masonite.helpers.Extendable import Extendable
from masonite.helpers.time import cookie_expire_time
from cryptography.fernet import InvalidToken


class Request(Extendable):
    """
    Handles many different aspects of a single request.
    This is the object passed through to the controllers
    as a request parameter
    """

    def __init__(self, environ=None):
        self.cookies = []
        self._headers = []
        self.url_params = {}
        self.redirect_url = False
        self.redirect_route = False
        self.user_model = None
        self.subdomain = None
        self._activate_subdomains = False
        self._status = '404 Not Found'

        if environ:
            self.load_environ(environ)

        self.encryption_key = False
        self.container = None

    def input(self, name, default=False):
        """
        Returns either the FORM_PARAMS during a POST request
        or QUERY_STRING during a GET request
        """
        return self.request_variables.get(name, default)

    def is_post(self):
        if self.environ['REQUEST_METHOD'] == 'POST':
            return True

        return False

    def is_not_get_request(self):
        if not self.environ['REQUEST_METHOD'] == 'GET':
            return True

        return False

    def __set_request_method(self):
        if self.has('__method'):
            self.environ['REQUEST_METHOD'] = self.input('__method')
            return True

        return False

    def key(self, key):
        """
        Sets encryption key
        """

        self.encryption_key = key
        return self

    def all(self, internal_variables=True):
        """
        Returns all the request variables
        """
        if not internal_variables:
            without_internals = {}
            for key, value in self.request_variables.items():
                if not key.startswith('__'):
                    without_internals.update({key: value})
            return without_internals
        
        return self.request_variables

    def only(self, *names):
        """
        Returns the specified request variables in a dictionary
        """
        only_vars = {}

        for name in names:
            only_vars[name] = self.request_variables.get(name)

        return only_vars

    def load_app(self, app):
        self.container = app
        return self

    def load_environ(self, environ):
        self.environ = environ
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.request_variables = {}

        self._set_standardized_request_variables(environ['QUERY_STRING'])

        if self.has('__method'):
            self.__set_request_method()

        return self

    def _set_standardized_request_variables(self, variables):
        if isinstance(variables, str):
            variables = parse_qs(variables)

        for name in variables.keys():
            value = self._get_standardized_value(variables[name])
            self.request_variables[name] = value

    def _get_standardized_value(self, value):
        if isinstance(value, list):
            return value[0]

        if isinstance(value, dict):
            return value

        if not value.filename:
            return value.value

        if value.filename:
            return value

        return False

    def app(self):
        return self.container

    def has(self, *args):
        """
        Check if a request variable exists
        """
        return all((arg in self.request_variables) for arg in args)

    def status(self, status):
        self.app().bind('StatusCode', status)
        return self

    def get_status_code(self):
        return self.app().make('StatusCode')
    
    def get_request_method(self):
        return self.environ['REQUEST_METHOD']

    def header(self, key, value=None, http_prefix=True):
        # Get Headers
        if value is None:
            if 'HTTP_{0}'.format(key) in self.environ:
                return self.environ['HTTP_{0}'.format(key)]
            elif key in self.environ:
                return self.environ[key]
            else:
                return None

        # Set Headers
        if http_prefix:
            self.environ['HTTP_{0}'.format(key)] = str(value)
            self._headers.append(('HTTP_{0}'.format(key), str(value)))
        else:
            self.environ[key] = str(value)
            self._headers.append((key, str(value)))
        return True

    def get_headers(self):
        return self._headers

    def reset_headers(self):
        self._headers = []

    def set_params(self, params):
        """
        Loads the params into the class.
        These parameters are where the developer can retrieve the
        /url/@variable:string/ from the url.
        """

        self.url_params.update(params)
        return self

    def param(self, parameter):
        """
        Retrieves the param from the URL.
        The "parameter" parameter in this method should be the name of the
        @variable passed into the url in web.py
        """

        if parameter in self.url_params:
            return self.url_params[parameter]
        return False

    def cookie(self, key, value, encrypt=True,
               http_only="HttpOnly;", path='/', expires=''):
        """
        Sets a cookie in the browser
        """

        if encrypt:
            value = Sign(self.encryption_key).sign(value)
        else:
            value = value

        if expires:
            expires = "Expires={0};".format(cookie_expire_time(expires))

        if not http_only:
            http_only = ""

        self.cookies.append(
            ('Set-Cookie', '{0}={1};{2} {3}Path={4}'.format(
                key, value, expires, http_only, path)))
        self.append_cookie(key, value)
        return self

    def get_cookies(self):
        """
        Retrieve all cookies from the browser
        """

        return self.cookies

    def get_cookie(self, provided_cookie, decrypt=True):
        """
        Retrieves a specific cookie from the browser
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
        if 'HTTP_COOKIE' in self.environ and self.environ['HTTP_COOKIE']:
            self.environ['HTTP_COOKIE'] += ';{0}={1}'.format(
                key, value)
        else:
            self.environ['HTTP_COOKIE'] = '{0}={1}'.format(
                key, value)

    def delete_cookie(self, key):
        """
        Delete cookie
        """
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
        """
        Loads the user into the class
        """

        self.user_model = user_model
        return self

    def user(self):
        """
        Retreives the user model
        """

        return self.user_model

    def redirect(self, route, params={}):
        """
        Redirect the user based on the route specified
        """
        self.redirect_url = self.compile_route_to_url(route, params)
        return self

    def redirect_to(self, route_name, params={}):
        """
        Redirect to a named route
        """
        web_routes = self.container.make('WebRoutes')

        self.redirect_url = self._get_named_route(route_name, params)

        return self
    
    def _get_named_route(self, name, params):
        web_routes = self.container.make('WebRoutes')

        for route in web_routes:
            if route.named_route == name:
                return self.compile_route_to_url(route.route_url, params)

        return None
    
    def _get_route_from_controller(self, controller):
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

    def url_from_controller(self, controller, params = {}):
        return self.compile_route_to_url(self._get_route_from_controller(controller).route_url, params)
    
    def route(self, name, params = {}):
        web_routes = self.container.make('WebRoutes')

        return self._get_named_route(name, params)

        return None

    def reset_redirections(self):
        self.redirect_url = False
        self.redirect_route = False

    def back(self, default=None):
        redirect_url = self.input('__back')
        if not redirect_url and default:
            return self.redirect(default)
        elif not redirect_url and not default:
            return self.redirect(self.path)  # Some global default?
        
        return self.redirect(redirect_url)
    
    def is_named_route(self, name, params={}):
        if self._get_named_route(name, params) == self.path:
            return True
        
        return False

    def contains(self, route):
        return re.match(compile_route_to_regex(route), self.path)

    def compile_route_to_url(self, route, params={}):
        """
        Compile the route url into a usable url
        Converts /url/@id into /url/1. Used for redirection
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
                    url = url.replace('@', '').replace(
                        ':int', '').replace(':string', '')
                    compiled_url += str(params[url]) + '/'
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
        self._activate_subdomains = True

    def has_subdomain(self):
        if self._activate_subdomains:
            url = tldextract.extract(self.environ['HTTP_HOST'])

            if url.subdomain:
                self.subdomain = url.subdomain
                self.url_params.update({'subdomain': self.subdomain})
                return True

        return False

    def send(self, params):
        """
        With
        """

        self.set_params(params)
        return self

    def helper(self):
        return self
    
    def pop(self, *input_variables):
        for key in input_variables:
            if key in self.request_variables:
                del self.request_variables[key]

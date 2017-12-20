''' Request Module handles many different aspects of a single request
    Methods which require the request and help ease development should
    be put here.

    Methods may return another object if necessary to expand capabilities
    of this class.
'''
from urllib.parse import parse_qs
from http import cookies

class Request(object):
    ''' Handles many different aspects of a single request.
        This is the object passed through to the controllers
        as a request paramter
    '''
    def __init__(self, environ):
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.cookies = []
        self.environ = environ
        self.params = parse_qs(environ['QUERY_STRING'])
        self.url_params = None
        self.redirect_url = False
        self.redirect_route = False

    def input(self, param):
        ''' Returns either the FORM_PARAMS during a POST request
            or QUERY_STRING during a GET request
        '''
        if self.has(param):
            return self.params[param][0]
        return False

    def all(self):
        ''' Returns all the params '''
        return self.params

    def has(self, param):
        ''' Check if a param exists '''
        if param in self.params:
            return True

        return False

    def set_params(self, params):
        ''' Loads the params into the class.
            These parameters are where the developer can retrieve the
            /url/@variable:string/ from the url.
        '''
        self.url_params = params
        return self

    def param(self, parameter):
        ''' Retrieves the param from the URL.
            The "parameter" parameter in this method should be the name of the @variable
            passed into the url in web.py '''
        if self.url_params[parameter]:
            return self.url_params[parameter]
        return False

    def cookie(self, key, value):
        ''' Sets a cookie in the browser '''
        self.cookies.append(('Set-Cookie', '{0}={1}'.format(key, value)))
        return self

    def get_cookies(self):
        ''' Retrieve all cookies from the browser '''
        return self.cookies

    def get_cookie(self, provided_cookie):
        ''' Retrieves a specific cookie from the browser '''
        if 'HTTP_COOKIE' in self.environ:
            grab_cookie = cookies.SimpleCookie(self.environ['HTTP_COOKIE'])
            if provided_cookie in grab_cookie:
                return grab_cookie[provided_cookie].value

        return None

    def redirect(self, route):
        ''' Redirect the user based on the route specified '''
        self.redirect_url = route
        return 'redirecting ...'

    def redirectTo(self, route):
        ''' Redirect to a named route '''
        self.redirect_route = route
        return 'redirecting ...'

''' Request Module handles many different aspects of a single request
    Methods which require the request and help ease development should
    be put here.

    Methods may return another object if necessary to expand capabilities
    of this class.
'''
from urllib.parse import parse_qs
from http import cookies
from masonite.auth.Sign import Sign

class Request(object):
    ''' Handles many different aspects of a single request.
        This is the object passed through to the controllers
        as a request paramter
    '''
    def __init__(self, environ):
        self.cookies = []
        self.url_params = None
        self.redirect_url = False
        self.redirect_route = False
        self.user_model = None
        self.environ = environ
        self.params = environ['QUERY_STRING']
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.encryption_key = False
        self.container = None

    def input(self, param):
        ''' Returns either the FORM_PARAMS during a POST request
            or QUERY_STRING during a GET request
        '''

        # Post Request Input
        if self.is_post():
            if isinstance(self.params, str):
                return parse_qs(self.params)[param][0]

            if not self.params[param].filename:
                return self.params[param].value

            if self.params[param].filename:
                return self.params[param]

        # Get Request Input
        if self.has(param):
            return parse_qs(self.params)[param][0]

        return False

    def file(self, param):
        pass

    def is_post(self):
        if self.environ['REQUEST_METHOD'] == 'POST':
            return True

        return False

    def key(self, key):
        ''' Sets encryption key '''
        self.encryption_key = key
        return self

    def all(self):
        ''' Returns all the params '''
        if isinstance(self.params, str):
            return parse_qs(self.params)
        
        return self.params

    def load_app(self, app):
        self.container = app
        return self

    def app(self):
        return self.container
    
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
        if parameter in self.url_params:
            return self.url_params[parameter]
        return False

    def cookie(self, key, value, encrypt = True):
        ''' Sets a cookie in the browser '''
        if encrypt:
            value = Sign(self.encryption_key).sign(value)
        else:
            value = value
            
        self.cookies.append(('Set-Cookie', '{0}={1}; HttpOnly'.format(key, value)))
        self.append_cookie(key, value)
        return self

    def get_cookies(self):
        ''' Retrieve all cookies from the browser '''
        return self.cookies

    def get_cookie(self, provided_cookie, decrypt=True):
        ''' Retrieves a specific cookie from the browser '''
        if 'HTTP_COOKIE' in self.environ:
            grab_cookie = cookies.SimpleCookie(self.environ['HTTP_COOKIE'])
            if provided_cookie in grab_cookie:
                if decrypt:
                    return Sign(self.encryption_key).unsign(
                        grab_cookie[provided_cookie].value)
                return grab_cookie[provided_cookie].value

        return None

    def append_cookie(self, key, value):
        if 'HTTP_COOKIE' in self.environ and self.environ['HTTP_COOKIE']:
            self.environ['HTTP_COOKIE'] += ';{0}={1}'.format(
                key, value)
        else:
            self.environ['HTTP_COOKIE'] = '{0}={1}'.format(
                key, value)

    def set_user(self, user_model):
        ''' Loads the user into the class '''
        self.user_model = user_model
        return self

    def user(self):
        ''' Retreives the user model '''
        return self.user_model

    def redirect(self, route):
        ''' Redirect the user based on the route specified '''
        self.redirect_url = route
        return self

    def redirectTo(self, route):
        ''' Redirect to a named route '''
        self.redirect_route = route
        return self

    def back(self, input_parameter='back'):
        ''' Go to a named route with the back parameter '''
        self.redirectTo(self.input(input_parameter))
        return self

    def compile_route_to_url(self):
        ''' Compile the route url into a usable url
            Converts /url/@id into /url/1. Used for redirection
        '''

        if 'http' in self.redirect_url:
            return self.redirect_url

        # Split the url into a list
        split_url = self.redirect_url.split('/')

        # Start beginning of the new compiled url
        compiled_url = '/'

        # Iterate over the list
        for url in split_url:

            # if the url contains a parameter variable like @id:int
            if '@' in url:
                url = url.replace('@', '').replace(':int', '').replace(':string', '')
                compiled_url += '/' + str(self.param(url))
            else:
                compiled_url += url

        return compiled_url

    def send(self, params):
        ''' With '''
        self.set_params(params)
        return self

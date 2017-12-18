import os
from urllib.parse import parse_qs
from http import cookies

class Request(object):

    def __init__(self, environ):
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.cookies = []
        parsed = parse_qs(environ['QUERY_STRING'])
        self.environ = environ
        self.params = parsed
        self.url_params = None

    def input(self, param):
        if self.has(param):
            return self.params[param][0]
        return False

    def all(self):
        return self.params

    def has(self, param):
        if param in self.params:
            return True
            
        return False

    def set_params(self, params):
        self.url_params = params
        return self

    def param(self, parameter):
        if self.url_params[parameter]:
            return self.url_params[parameter]
        return False

    def cookie(self, key, value):
        self.cookies.append(('Set-Cookie', '{0}={1}'.format(key, value)))
        return self

    def get_cookies(self):
        return self.cookies

    def get_cookie(self, provided_cookie):
        # for key, value in enumerate(self.cookies):
        #     if cookie in self.cookies[key][1]:
        #         return self.cookies[key]
        # return None

        if 'HTTP_COOKIE' in self.environ:
            grab_cookie = cookies.SimpleCookie(self.environ['HTTP_COOKIE'])
            if provided_cookie in grab_cookie:
                return grab_cookie[provided_cookie].value

        return None
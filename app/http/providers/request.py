import os
from urlparse import urlparse, parse_qs
import shelve

class Request(object):

    def __init__(self, environ):
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        parsed = parse_qs(environ['QUERY_STRING'])
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

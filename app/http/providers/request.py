import os
from urlparse import urlparse, parse_qs
import shelve

class Request(object):

    def __init__(self, environ):
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        parsed = parse_qs(environ['QUERY_STRING'])
        self.params = parsed

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

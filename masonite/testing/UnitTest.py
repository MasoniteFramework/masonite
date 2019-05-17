import io
import json
import sys
import unittest
from contextlib import contextmanager

from masonite.testing import MockJson, MockRequest, MockRoute
from masonite.testsuite import TestSuite, generate_wsgi

from _io import StringIO

# from masonite.testing.MockJson import MockJson


class UnitTest(unittest.TestCase):

    def setUp(self):
        self.container = TestSuite().create_container().container

    def get(self, url):
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = url
        self.container = TestSuite().create_container(wsgi=wsgi).container
        return MockRequest(url, self.container)

    def route(self, url, method=False):
        for route in self.container.make('WebRoutes'):
            if route.route_url == url and (method in route.method_type or not method):
                return MockRoute(route, self.container)

    def routes(self, routes):
        self.container.bind('WebRoutes', self.container.make('WebRoutes') + routes)

    def json(self, url, data, method=['POST']):
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = url
        wsgi['CONTENT_TYPE'] = 'application/json'
        wsgi['REQUEST_METHOD'] = method
        wsgi['CONTENT_LENGTH'] = len(str(json.dumps(data)))
        wsgi['wsgi.input'] = io.StringIO(json.dumps(data))
        self.container = TestSuite().create_container(wsgi=wsgi).container
        return MockJson(url, self.container)

    @contextmanager
    def captureOutput(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

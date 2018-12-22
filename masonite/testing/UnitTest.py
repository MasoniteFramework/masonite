from masonite.testsuite import TestSuite, generate_wsgi
from masonite.testing import MockRoute, MockRequest, MockJson
import json
import io
# from masonite.testing.MockJson import MockJson


class UnitTest:

    def setup_method(self):
        self.container = TestSuite().create_container().container

    def controller(self):
        pass

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

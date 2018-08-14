from masonite.testsuite import TestSuite, generate_wsgi
from masonite.testing import MockRoute, MockRequest

class UnitTest:

    def setup_method(self):
        self.container = TestSuite().create_container().container

    def controller(self): pass

    def get(self, url): 
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = url
        self.container = TestSuite().create_container(wsgi=wsgi).container
        return MockRequest(url, self.container)

    def route(self, url, method='GET'):
        for route in self.container.make('WebRoutes'):
            if route.route_url == url and route.method_type == method:
                return MockRoute(route, self.container)

    def routes(self, routes): 
        self.container.bind('WebRoutes', self.container.make('WebRoutes') + routes)

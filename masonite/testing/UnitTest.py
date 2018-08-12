from masonite.testsuite import TestSuite
from masonite.testing import MockRoute

class UnitTest:

    def setup_method(self):
        self.container = TestSuite().create_container().container

    def controller(self): pass

    def route(self, url, method='GET'):
        for route in self.container.make('WebRoutes'):
            if route.route_url == url and route.method_type == method:
                return MockRoute(route, self.container)

    def routes(self, routes): 
        self.container.bind('WebRoutes', self.container.make('WebRoutes') + routes)

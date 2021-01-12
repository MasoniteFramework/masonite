from unittest import TestCase

class HTTPRoute:

    def __init__(self, url, controller=None, request_method="get"):
        self.url = url
        self.controller = controller
        self.request_method = request_method

class Route:
    
    routes = []

    def __init__(self):
        pass

    @classmethod
    def add(self, route):
        self.routes.append(route)
        return self

    @classmethod
    def get(self, url, controller, **options):
        self.routes.append(HTTPRoute(url, controller, request_method=["get"], **options))
        return self

    @classmethod
    def post(self, url, controller, **options):
        self.routes.append(HTTPRoute(url, controller, request_method=["post"], **options))
        return self

    @classmethod
    def put(self, url, controller, **options):
        self.routes.append(HTTPRoute(url, controller, request_method=["put"], **options))
        return self

    @classmethod
    def patch(self, url, controller, **options):
        self.routes.append(HTTPRoute(url, controller, request_method=["patch"], **options))
        return self

    @classmethod
    def delete(self, url, controller, **options):
        self.routes.append(HTTPRoute(url, controller, request_method=["delete"], **options))
        return self

    @classmethod
    def option(self, url, controller, **options):
        self.routes.append(HTTPRoute(url, controller, request_method=["post"], **options))
        return self

    @classmethod
    def match(self, url, controller, **options):
        self.routes.append(HTTPRoute(url, controller, request_method=["post"], **options))
        return self

    def find(self, path):
        return

class TestRoutes(TestCase):

    def test_can_add_routes(self):
        Route.get('/home', 'TestController')
        Route.get('/login', 'TestController')
        self.assertEqual(len(Route.routes), 2)
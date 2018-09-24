from masonite.routes import Get
from routes import web


class TestRoute:

    def __init__(self, route):
        self.route = None

        for routes in web.ROUTES:
            if routes.route_url == route:
                self.route = routes
                break

    def exists(self):
        return isinstance(self.route, Get)

    def has_middleware(self, middleware):
        return middleware in self.route.list_middleware

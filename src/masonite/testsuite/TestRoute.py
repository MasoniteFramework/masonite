from masonite.routes import Get


class TestRoute:

    def __init__(self, route):
        self.route = None
        from routes import web
        for routes in web.ROUTES:
            if routes.route_url == route:
                self.route = routes
                break

    def exists(self):
        return isinstance(self.route, Get)

    def hasMiddleware(self, middleware):
        return middleware in self.route.list_middleware

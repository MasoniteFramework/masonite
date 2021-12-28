class MiddlewareCapsule:
    def __init__(self):
        self.route_middleware = {}
        self.http_middleware = []

    def add(self, middleware):
        if isinstance(middleware, dict):
            self.route_middleware.update(middleware)

        if isinstance(middleware, list):
            self.http_middleware += middleware

        return self

    def remove(self, middleware):
        if middleware in self.route_middleware:
            self.route_middleware.pop(middleware)
        elif middleware in self.http_middleware:
            self.http_middleware.pop(self.http_middleware.index(middleware))
        return self

    def get_route_middleware(self, keys=None):
        middlewares = []
        if keys is None:
            return self.route_middleware

        if keys is None:
            keys = []

        for key in keys:
            found = self.route_middleware[key]
            if isinstance(found, list):
                middlewares += found
            else:
                middlewares += [found]
        return middlewares

    def get_http_middleware(self):
        return self.http_middleware

    def run_route_middleware(self, middlewares, request, response, callback="before"):
        for middleware in middlewares:
            if ":" in middleware:
                # get list of arguments if any
                middleware_to_run, raw_arguments = middleware.split(":")
                raw_arguments = raw_arguments.split(",")
                # try to parse arguments with @ from requests
                arguments = []
                for arg in raw_arguments:
                    if "@" in arg:
                        arg = arg.replace("@", "")
                        arg = request.input(arg)
                    arguments.append(arg)
                arguments = tuple(arguments)
            else:
                middleware_to_run = middleware
                arguments = ()
            route_middlewares = self.get_route_middleware([middleware_to_run])
            for route_middleware in route_middlewares:
                middleware_response = getattr(route_middleware(), callback)(
                    request, response, *arguments
                )
                if middleware_response != request:
                    return False
        return True

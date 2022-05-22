from typing import TYPE_CHECKING, List

from ..exceptions import RouteMiddlewareNotFound

if TYPE_CHECKING:
    from .middleware import Middleware
    from ..request import Request
    from ..response import Response


class MiddlewareCapsule:
    """MiddlewareCapsule class used to manage all HTTP and routes middleware of the application."""

    def __init__(self):
        self.route_middleware: dict = {}
        self.http_middleware: list = []

    def add(self, middleware: "dict|list") -> "MiddlewareCapsule":
        """Add HTTP or routes middlewares."""
        if isinstance(middleware, dict):
            self.route_middleware.update(middleware)

        if isinstance(middleware, list):
            self.http_middleware += middleware

        return self

    def remove(self, middleware: "Middleware") -> "MiddlewareCapsule":
        """Remove a configured Middleware from HTTP or Routes middlewares."""
        if middleware in self.route_middleware:
            self.route_middleware.pop(middleware)
        elif middleware in self.http_middleware:
            self.http_middleware.pop(self.http_middleware.index(middleware))
        return self

    def get_route_middleware(self, keys: list = None) -> "List[Middleware]":
        """Get all Route middlewares or a subset of the route middlewares from the given keys."""
        middlewares = []
        if keys is None:
            return self.route_middleware

        for key in keys:
            try:
                found = self.route_middleware[key]
            except KeyError:
                raise RouteMiddlewareNotFound(
                    f"Could not find the '{key}' middleware key."
                )
            if isinstance(found, list):
                middlewares += found
            else:
                middlewares += [found]
        return middlewares

    def get_http_middleware(self) -> "List[Middleware]":
        """Get all HTTP middlewares."""
        return self.http_middleware

    def run_route_middleware(
        self,
        middlewares: "List[Middleware]",
        request: "Request",
        response: "Response",
        callback: str = "before",
    ) -> bool:
        """Run the given route middlewares callback. Callback can be 'before' or 'after'."""
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

from urllib import parse
from ..utils.collections import flatten
from ..exceptions import RouteNotFoundException, MethodNotAllowedException


class Router:

    http_methods = ["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

    def __init__(self, *routes, module_location=None):
        self.routes = flatten(routes)

    def find(self, path, request_method, subdomain=None):
        from .HTTPRoute import HTTPRoute

        for route in self.routes:
            if route.match(path, request_method, subdomain=subdomain):
                return route

        # we did not find a route matching the given path and method.
        # we will try to find a route matching other methods
        other_methods = [
            method for method in self.http_methods if method != request_method
        ]
        matched_methods = []
        for other_method in other_methods:
            for route in self.routes:
                if route.match(path, other_method, subdomain=subdomain):
                    matched_methods.append(other_method)
                    break

        # we really did not find a route
        if not matched_methods:
            return None

        # if alternative methods have been found, check if current request method is OPTIONS
        # to build a proper response else build a method not allowed response
        if request_method == "OPTIONS":
            def preflight_response(app):
                return (
                    app.make("response")
                    .with_headers({"Allow": ", ".join(matched_methods)})
                    .status(204)
                )

            preflight_route = HTTPRoute(path, request_method=["options"])
            preflight_route.get_response = preflight_response
            return preflight_route
        else:
            raise MethodNotAllowedException(matched_methods, request_method)

    def matches(self, path):
        for route in self.routes:
            if route.matches(path):
                return route

    def find_by_name(self, name):
        for route in self.routes:
            if route.match_name(name):
                return route

    def route(self, name: str, parameters: dict = {}, query_params: dict = {}) -> str:
        """Return URL string from given route name and parameters."""
        route = self.find_by_name(name)
        if route:
            return route.to_url(parameters, query_params)
        raise RouteNotFoundException(f"Could not find route with the name '{name}'")

    def set_controller_locations(self, location):
        self.controller_locations = location
        return self

    def add(self, *routes):
        self.routes.append(*routes)
        self.routes = flatten(self.routes)

    def set(self, *routes):
        self.routes = []
        self.routes.append(*routes)
        self.routes = flatten(self.routes)

    @classmethod
    def compile_to_url(cls, uncompiled_route, params={}, query_params={}):
        """Compile the route url into a usable url: converts /url/@id into /url/1.
        Used for redirection

        Arguments:
            route {string} -- An uncompiled route like (/dashboard/@user:string/@id:int)
        Keyword Arguments:
            params {dict} -- Dictionary of parameters to pass to the route (default: {{}})
            query_params {dict} -- Dictionary of query parameters to pass to the route (default: {{}})
        Returns:
            string -- Returns a compiled string (/dashboard/joseph/1)
        """
        if "http" in uncompiled_route:
            return uncompiled_route

        # Split the url into a list
        split_url = uncompiled_route.split("/")

        # Start beginning of the new compiled url
        compiled_url = "/"

        # Iterate over the list
        for url in split_url:
            if url:
                # if the url contains a parameter variable like @id:int
                if "@" in url:
                    url = url.replace("@", "").split(":")[0]
                    if isinstance(params, dict):
                        compiled_url += str(params[url]) + "/"
                    elif isinstance(params, list):
                        compiled_url += str(params.pop(0)) + "/"
                elif "?" in url:
                    url = url.replace("?", "").split(":")[0]
                    if isinstance(params, dict):
                        compiled_url += str(params.get(url, "/")) + "/"
                    elif isinstance(params, list):
                        compiled_url += str(params.pop(0)) + "/"
                else:
                    compiled_url += url + "/"

        compiled_url = compiled_url.replace("//", "")
        # The loop isn't perfect and may have an unwanted trailing slash
        if compiled_url.endswith("/") and not uncompiled_route.endswith("/"):
            compiled_url = compiled_url[:-1]

        # The loop isn't perfect and may have 2 slashes next to eachother
        if "//" in compiled_url:
            compiled_url = compiled_url.replace("//", "/")

        # Add eventual query parameters
        if query_params:
            compiled_url += "?" + parse.urlencode(query_params)

        return compiled_url

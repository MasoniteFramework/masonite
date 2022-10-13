import re
from urllib import parse

from ..utils.str import modularize, removeprefix
from ..exceptions import InvalidRouteCompileException
from ..facades import Loader
from ..controllers import Controller
from ..exceptions import LoaderNotFound


class HTTPRoute:

    _base_casts_map = {
        "int": int,
        "integer": int,
        "string": str,
        "str": str,
        "float": float,
    }

    def __init__(
        self,
        url,
        controller=None,
        request_method=["get"],
        name=None,
        compilers=None,
        controllers_locations=["app.http.controllers"],
        controller_bindings=[],
        **options,
    ):
        if not url.startswith("/"):
            url = "/" + url
        if url.endswith("/") and url != "/":
            url = url[:-1]

        self.url = url
        self.controllers_locations = controllers_locations
        self.controller = controller
        self.controller_class = None
        self.controller_instance = None
        self.controller_method = None
        self._domain = None
        self._name = name
        self._casts_map = {}
        self._active_regex = {}
        self._should_cast = False

        self.request_method = [x.lower() for x in request_method]
        # add HEAD method if GET
        if "get" in self.request_method and "head" not in self.request_method:
            self.request_method.append("head")

        self.list_middleware = []
        self.excluded_middlewares = []
        self.e = None
        self.compilers = compilers or {}
        self._find_controller(controller)
        self.controller_bindings = controller_bindings
        self.compile_route_to_regex()

    def __str__(self):
        return f"<HttpRoute [{self._name}]: {self.url}>"

    def match(self, path, request_method, subdomain=None):

        route_math = (
            re.match(self._compiled_regex, path)
            or re.match(self._compiled_regex_end, path)
        ) and request_method.lower() in self.request_method

        domain_match = subdomain == self._domain

        return route_math and domain_match

    def get_name(self):
        return self._name

    def matches(self, path):
        return re.match(self._compiled_regex, path) or re.match(
            self._compiled_regex_end, path
        )

    def match_name(self, name):
        return name == self._name

    def name(self, name):
        self._name = name
        return self

    def domain(self, subdomain):
        self._domain = subdomain
        return self

    def to_url(self, parameters: dict = {}, query_params: dict = {}) -> str:
        """Transform route to a URL string with the given url and query parameters."""

        # Split the url into a list
        split_url = self.url.split("/")

        # Start beginning of the new compiled url
        compiled_url = "/"

        # Iterate over the list
        for url in split_url:
            if url:
                # if the url contains a parameter variable like @id:int
                if "@" in url:
                    url = url.replace("@", "").split(":")[0]
                    if isinstance(parameters, dict):
                        compiled_url += str(parameters[url]) + "/"
                    elif isinstance(parameters, list):
                        compiled_url += str(parameters.pop(0)) + "/"
                elif "?" in url:
                    url = url.replace("?", "").split(":")[0]
                    if isinstance(parameters, dict):
                        compiled_url += str(parameters.get(url, "/")) + "/"
                    elif isinstance(parameters, list):
                        compiled_url += str(parameters.pop(0)) + "/"
                else:
                    compiled_url += url + "/"

        # The loop isn't perfect and may have an unwanted trailing slash
        if compiled_url.endswith("/"):
            compiled_url = compiled_url[:-1]

        # The loop isn't perfect and may have 2 slashes next to eachother
        if "//" in compiled_url:
            compiled_url = compiled_url.replace("//", "/")

        # Add eventual query parameters
        if query_params:
            compiled_url += "?" + parse.urlencode(query_params)
        return compiled_url

    def _find_controller(self, controller):
        """Find the controller to attach to the route. Look for controller (str or class) in all
        specified controllers_location.

        Arguments:
            controller {string|object} -- String or object controller to search for.

        Returns:
            None
        """
        if controller is None:
            return None
        # If the output specified is a string controller e.g. "WelcomeController@show"
        elif isinstance(controller, str):
            if "@" in controller:
                controller_path, controller_method_str = controller.split("@")
            else:
                controller_path = controller
                controller_method_str = "__call__"

            controller_path = modularize(controller_path).split(".")
            if len(controller_path) > 1:
                controller_name = controller_path.pop()
                prefix_path = ".".join(controller_path)
            else:
                controller_name = controller_path[0]
                prefix_path = ""
            # build a list of all locations where the controller can be found
            # if the controller is defined such as auth.WelcomeController, append the prefix path to
            # the locations
            locations = list(
                map(
                    lambda loc: f"{loc}.{removeprefix(prefix_path, loc)}"
                    if prefix_path
                    else loc,
                    self.controllers_locations,
                )
            )
            try:
                self.controller_class = Loader.find(
                    Controller, locations, controller_name, raise_exception=True
                )
            except LoaderNotFound as e:
                self.e = e
                print(f"\033[93mTrouble importing controller!\n> {str(e)}\033[0m")
        # controller is an instance with a bound method
        elif hasattr(controller, "__self__"):
            _, controller_method_str = controller.__qualname__.split(".")
            self.controller_instance = controller.__self__

        # it's a class or class.method, we don't have to find it, just get the class
        elif hasattr(controller, "__qualname__"):
            if "." in controller.__qualname__:
                controller_name, controller_method_str = controller.__qualname__.split(
                    "."
                )
            else:
                controller_name = controller.__qualname__
                controller_method_str = "__call__"

            try:
                self.controller_class = Loader.get_object(
                    controller.__module__, controller_name, raise_exception=True
                )
            except LoaderNotFound as e:
                self.e = e
                print(f"\033[93mTrouble importing controller!\n> {str(e)}\033[0m")
        # it's a controller instance
        else:
            self.controller_instance = controller
            controller_method_str = "__call__"

        # Set the controller method on class. This is a string
        self.controller_method = controller_method_str

    def get_response(self, app=None):
        from ..response import Response

        # Resolve Controller Constructor
        if self.e:
            print(
                "\033[93mCannot find controller {}. Did you create this one?".format(
                    self.controller
                ),
                "\033[0m",
            )
            raise SyntaxError(str(self.e))

        if app:
            if self.controller_instance:
                controller = self.controller_instance
            else:
                controller = app.resolve(
                    self.controller_class, *self.controller_bindings
                )
            # resolve route parameters
            params = self.extract_parameters(app.make("request").get_path()).values()
            # Resolve Controller Method
            response = app.resolve(getattr(controller, self.controller_method), *params)

            # if request method is HEAD, return a response without content but with
            # headers that would be returned if request's URL was requested with GET method instead
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD
            if app.make("request").get_request_method().upper() == "HEAD":
                real_response = app.make("response").view(response)
                response = Response(app).status(204)
                response.header_bag = real_response.header_bag
                app.bind("response", response)
            return response

        if self.controller_instance:
            controller = self.controller_instance
        else:
            controller = self.controller_class(*self.controller_bindings)

        return getattr(controller, self.controller_method)()

    def middleware(self, *args):
        """Load a list of middleware to run.

        Returns:
            self
        """
        for arg in args:
            if arg and arg not in self.list_middleware:
                self.list_middleware.append(arg)
        return self

    def prepend_middleware(self, *args):
        """Load a list of middleware to run.

        Returns:
            self
        """
        for arg in args:
            if arg and arg not in self.list_middleware:
                self.list_middleware.insert(0, arg)
        return self

    def get_middlewares(self):
        """Get all the middlewares to run for this route."""
        middlewares = self.list_middleware

        for middleware in self.excluded_middlewares:
            if middleware in middlewares:
                middlewares.remove(middleware)

        return middlewares

    def set_middleware(self, middleware):
        """Get all the middlewares to run for this route."""
        self.list_middleware = middleware

        return self

    def exclude_middleware(self, *args):
        """Remove a list of middleware for this route. It can be useful when
        using Route group middleware to override middleware for a given route in the group."""
        for middleware in args:
            self.excluded_middlewares.append(middleware)
        return self

    def compile_route_to_regex(self):
        """Compile the given route to a regex string.

        Arguments:
            route {string} -- URI of the route to compile.

        Returns:
            string -- Compiled URI string.
        """
        # Split the route
        split_given_route = self.url.split("/")
        # compile the provided url into regex
        url_list = []
        regex = "^"
        for regex_route in split_given_route:
            if "@" in regex_route:
                if ":" in regex_route:
                    try:
                        param_name, compiler_name = regex_route.split(":")
                        regex += self.compilers[compiler_name]
                        self._active_regex.update(
                            {param_name.replace("@", ""): compiler_name}
                        )
                    except KeyError:
                        raise InvalidRouteCompileException(
                            'Route compiler "{}" is not an available route compiler. '
                            "Verify you spelled it correctly or that you have added it using the compile() method.".format(
                                regex_route.split(":")[1]
                            )
                        )

                else:
                    regex += self.compilers["default"]

                regex += r"\/"

                # append the variable name passed @(variable):int to a list
                url_list.append(regex_route.replace("@", "").split(":")[0])
            elif "?" in regex_route:
                # Make the preceding token match 0 or more
                regex += "?"

                if ":" in regex_route:

                    try:
                        param_name, compiler_name = regex_route.split(":")
                        regex += self.compilers[compiler_name] + "*"
                        self._active_regex.update(
                            {param_name.replace("@", ""): compiler_name}
                        )
                    except KeyError:
                        if self.request:
                            raise InvalidRouteCompileException(
                                'Route compiler "{}" is not an available route compiler. '
                                "Verify you spelled it correctly or that you have added it using the compile() method.".format(
                                    regex_route.split(":")[1]
                                )
                            )
                        self._compiled_regex = None
                        self._compiled_regex_end = None
                        return

                else:
                    regex += self.compilers["default"] + "*"

                regex += r"\/"

                url_list.append(regex_route.replace("?", "").split(":")[0])
            else:
                regex += regex_route + r"\/"

        self.url_list = url_list
        regex += "$"
        self._compiled_regex = re.compile(regex.replace(r"\/$", r"$"))
        self._compiled_regex_end = re.compile(regex)

        return regex

    def extract_parameters(self, path):
        if not self.url_list:
            return {}

        if (not path.endswith("/")) or path == "/":
            matching_regex = self._compiled_regex
        else:
            matching_regex = self._compiled_regex_end
        params = dict(zip(self.url_list, matching_regex.match(path).groups()))

        if self._should_cast:
            for param, value in params.items():
                # get cast type from cast map if defined else use cast type from compiler else str
                cast_type = self._casts_map.get(
                    param,
                    self._base_casts_map.get(self._active_regex.get(param), str),
                )
                params.update({param: cast_type(value)})
        return params

    def casts(self, _casts_map: dict = {}) -> "HTTPRoute":
        self._casts_map = _casts_map
        self._should_cast = True
        return self

import importlib
import re

from ..exceptions import InvalidRouteCompileException, RouteMiddlewareNotFound


class HTTPRoute:
    def __init__(
        self, url, controller=None, request_method=["get"], name=None, compilers=None
    ):
        self.url = url
        self.module_location = "app.http.controllers"
        self.controller = controller
        self._domain = None
        self._name = name
        self.request_method = [x.lower() for x in request_method]
        self.list_middleware = []
        self.e = None
        self.compilers = compilers or {}
        self._find_controller(controller)
        self.compile_route_to_regex()

    def match(self, path, request_method, subdomain=None):
        route_math = (
            re.match(self._compiled_regex, path)
            or re.match(self._compiled_regex_end, path)
            and request_method.lower() in self.request_method
        )

        print(subdomain, self._domain)
        domain_match = subdomain == self._domain

        return route_math and domain_match

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

    def _find_controller(self, controller):
        """Find the controller to attach to the route.

        Arguments:
            controller {string|object} -- String or object controller to search for.

        Returns:
            None
        """
        module_location = self.module_location
        # If the output specified is a string controller
        if isinstance(controller, str):
            mod = controller.split("@")
            # If trying to get an absolute path via a string
            if mod[0].startswith("/"):
                module_location = ".".join(mod[0].replace("/", "").split(".")[0:-1])
            elif "." in mod[0]:
                # This is a deeper module controller
                module_location += "." + ".".join(mod[0].split(".")[:-1])
        else:
            if controller is None:
                return None

            fully_qualified_name = controller.__qualname__
            mod = fully_qualified_name.split(".")
            module_location = controller.__module__

        # Gets the controller name from the output parameter
        # This is used to add support for additional modules
        # like 'LoginController' and 'Auth.LoginController'
        get_controller = mod[0].split(".")[-1]

        try:
            # Import the module
            if isinstance(controller, str):
                module = importlib.import_module(
                    "{0}.".format(module_location) + get_controller
                )
            else:
                module = importlib.import_module("{0}".format(module_location))

            # Get the controller from the module
            self.controller_class = getattr(module, get_controller)

            # Set the controller method on class. This is a string
            self.controller_method = mod[1] if len(mod) == 2 else "__call__"
        except ImportError as e:
            import sys
            import traceback

            _, _, exc_tb = sys.exc_info()
            self.e = e
        except Exception as e:  # skipcq
            import sys
            import traceback

            _, _, exc_tb = sys.exc_info()
            self.e = e
            print("\033[93mTrouble importing controller!", str(e), "\033[0m")
        if not self.e:
            self.module_location = module_location

    def get_response(self, app=None):
        # Resolve Controller Constructor
        if self.e:
            print(
                "\033[93mCannot find controller {}. Did you create this one?".format(
                    self.output
                ),
                "\033[0m",
            )
            raise SyntaxError(str(self.e))

        if app:
            controller = app.resolve(self.controller_class)
            print("cc", controller)
            # Resolve Controller Method
            response = app.resolve(
                getattr(controller, self.controller_method),
                # *self.request.url_params.values() TODO
            )

        if hasattr(response, "rendered_template"):
            response = response.rendered_template

        return response

    def middleware(self, *args):
        """Load a list of middleware to run.

        Returns:
            self
        """
        for arg in args:
            if arg not in self.list_middleware:
                self.list_middleware.append(arg)

        return self

    def run_middleware(self, type_of_middleware):
        """Run route middleware.

        Arguments:
            type_of_middleware {string} -- Type of middleware to be ran (before|after)

        Raises:
            RouteMiddlewareNotFound -- Thrown when the middleware could not be found.
        """
        # Get the list of middleware to run for a route.
        for arg in self.list_middleware:
            if ":" in arg:
                middleware_to_run, arguments = arg.split(":")
                # Splits "name:value1,value2" into ['value1', 'value2']
                arguments = arguments.split(",")
                for index, argument in enumerate(arguments):
                    if argument.startswith("@"):
                        _, argument = argument.split("@")
                        arguments[index] = self.request.param(argument)
            else:
                middleware_to_run = arg
                arguments = []

            middleware_to_run = self.request.app().make("RouteMiddleware")[
                middleware_to_run
            ]
            if not isinstance(middleware_to_run, list):
                middleware_to_run = [middleware_to_run]

            try:
                for middleware in middleware_to_run:
                    located_middleware = self.request.app().resolve(middleware)
                    if hasattr(located_middleware, type_of_middleware):
                        getattr(located_middleware, type_of_middleware)(*arguments)
            except KeyError:
                raise RouteMiddlewareNotFound(
                    "Could not find the '{0}' route middleware".format(arg)
                )

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
                        regex += self.compilers[regex_route.split(":")[1]]
                    except KeyError:
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
                    regex += self.compilers["default"]

                regex += r"\/"

                # append the variable name passed @(variable):int to a list
                url_list.append(regex_route.replace("@", "").split(":")[0])
            elif "?" in regex_route:
                # Make the preceding token match 0 or more
                regex += "?"

                if ":" in regex_route:

                    try:
                        regex += self.compilers[regex_route.split(":")[1]] + "*"
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
        if not path.endswith("/"):
            matching_regex = self._compiled_regex
        elif path == "/":
            matching_regex = self._compiled_regex
        else:
            matching_regex = self._compiled_regex_end
        try:
            parameter_dict = {}
            print(path, matching_regex)
            for index, value in enumerate(matching_regex.match(path).groups()):
                parameter_dict[
                    self.url_list[index]
                ] = value or self.get_default_parameter(self.url_list[index])
            return parameter_dict
        except AttributeError as e:
            # raise e
            pass

        return {}

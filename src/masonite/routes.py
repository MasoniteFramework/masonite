"""Module for the Routing System."""

import cgi
import importlib
import json
import re

from .exceptions import (
    RouteMiddlewareNotFound,
    InvalidRouteCompileException,
    RouteException,
)
from .view import View


class Route:
    """Route class used to handle routing."""

    route_compilers = {
        "int": r"(\d+)",
        "integer": r"(\d+)",
        "string": r"([a-zA-Z]+)",
        "default": r"([\w.-]+)",
        "signed": r"([\w\-=]+)",
    }

    def __init__(self, environ=None):
        """Route constructor.

        Keyword Arguments:
            environ {dict} -- WSGI environ (default: {None})
        """
        self.url_list = []
        self.method_type = ["GET"]

        if environ:
            self.load_environ(environ)

    def load_environ(self, environ):
        """Load the WSGI environ into the class.

        Arguments:
            environ {dict} -- WSGI environ

        Returns:
            self
        """
        self.environ = environ
        self.url = environ["PATH_INFO"]

        return self

    def is_post(self):
        """Check to see if the current request is a POST request.

        Returns:
            bool
        """
        if self.environ["REQUEST_METHOD"] == "POST":
            return True

        return False

    def is_not_get_request(self):
        """Check if current request is not a get request.

        Returns:
            bool
        """
        if not self.environ["REQUEST_METHOD"] == "GET":
            return True

        return False

    def compile(self, key, to=""):
        self.route_compilers.update({key: to})
        return self

    def generated_url_list(self):
        """Return the URL list.

        Returns:
            list -- URL list.
        """
        return self.url_list


class BaseHttpRoute:
    """Base route for HTTP routes."""

    def __init__(self):
        self.method_type = ["GET"]
        self.output = False
        self.route_url = None
        self.request = None
        self.named_route = None
        self.required_domain = None
        self.module_location = "app.http.controllers"
        self.list_middleware = []
        self.default_parameters = {}
        self.e = False

    def default(self, dictionary):
        self.default_parameters.update(dictionary)
        return self

    def get_default_parameter(self, key):
        return self.default_parameters.get(key, None)

    def route(self, route, output):
        """Load the route into the class. This also looks for the controller and attaches it to the route.

        Arguments:
            route {string} -- This is a URI to attach to the route (/dashboard/user).
            output {string|object} -- Controller to attach to the route.

        Returns:
            self
        """
        self.output = output
        self._find_controller(output)

        if not route.startswith("/"):
            route = "/" + route

        if route.endswith("/") and route != "/":
            route = route[:-1]

        self.route_url = route
        self._compiled_url = self.compile_route_to_regex()
        return self

    def view(self, route, template, dictionary={}):
        view_route = ViewRoute(self.method_type, route, template, dictionary)
        return view_route

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
            self.controller = getattr(module, get_controller)

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

    def get_response(self):
        # Resolve Controller Constructor
        if self.e:
            print(
                "\033[93mCannot find controller {}. Did you create this one?".format(
                    self.output
                ),
                "\033[0m",
            )
            raise SyntaxError(str(self.e))

        controller = self.request.app().resolve(self.controller)

        # Resolve Controller Method
        response = self.request.app().resolve(
            getattr(controller, self.controller_method),
            *self.request.url_params.values()
        )

        if isinstance(response, View):
            response = response.rendered_template

        return response

    def domain(self, domain):
        """Set the subdomain for the route.

        Arguments:
            domain {string|list|tuple} -- The string or list of subdomains to attach to this route.

        Returns:
            self
        """
        self.required_domain = domain
        return self

    def module(self, module):
        """DEPRECATED :: The base module to look for string controllers.

        Arguments:
            module {string} -- The string representation of a module to look for controllers.

        Returns:
            self
        """
        self.module_location = module
        return self

    def has_required_domain(self):
        """Check if the route has the required subdomain before executing the route.

        Returns:
            bool
        """
        if self.request.has_subdomain() and (
            self.required_domain == "*"
            or self.request.subdomain == self.required_domain
        ):
            return True
        return False

    def name(self, name):
        """Specify the name of the route.

        Arguments:
            name {string} -- Sets a name for the route.

        Returns:
            self
        """
        self.named_route = name
        return self

    def load_request(self, request):
        """Load the request into this class.

        Arguments:
            request {masonite.request.Request} -- Request object.

        Returns:
            self
        """
        self.request = request
        return self

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
        split_given_route = self.route_url.split("/")
        # compile the provided url into regex
        url_list = []
        regex = "^"
        for regex_route in split_given_route:
            # if not regex_route:
            #     continue
            if "@" in regex_route:
                if ":" in regex_route:
                    try:
                        regex += Route.route_compilers[regex_route.split(":")[1]]
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
                    regex += Route.route_compilers["default"]

                regex += r"\/"

                # append the variable name passed @(variable):int to a list
                url_list.append(regex_route.replace("@", "").split(":")[0])
            elif "?" in regex_route:
                # Make the preceding token match 0 or more
                regex += "?"

                if ":" in regex_route:

                    try:
                        regex += Route.route_compilers[regex_route.split(":")[1]] + "*"
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
                    regex += Route.route_compilers["default"] + "*"

                regex += r"\/"

                url_list.append(regex_route.replace("?", "").split(":")[0])
            else:
                regex += regex_route + r"\/"

        self.url_list = url_list
        regex += "$"
        self._compiled_regex = re.compile(regex.replace(r"\/$", r"$"))
        self._compiled_regex_end = re.compile(regex)

        return regex


class Get(BaseHttpRoute):
    """Class for specifying GET requests."""

    def __init__(self, route=None, output=None):
        """Get constructor."""
        super().__init__()
        self.method_type = ["GET"]
        # self.list_middleware = []
        if route is not None and output is not None:
            self.route(route, output)


class Head(BaseHttpRoute):
    """Class for specifying HEAD requests."""

    def __init__(self, route=None, output=None):
        """Head constructor."""
        super().__init__()
        self.method_type = ["HEAD"]
        if route is not None and output is not None:
            self.route(route, output)


class Post(BaseHttpRoute):
    """Class for specifying POST requests."""

    def __init__(self, route=None, output=None):
        """Post constructor."""
        super().__init__()
        self.method_type = ["POST"]
        if route is not None and output is not None:
            self.route(route, output)


class Match(BaseHttpRoute):
    """Class for specifying Match requests."""

    def __init__(self, method_type=["GET"], route=None, output=None):
        """Match constructor."""
        super().__init__()
        if not isinstance(method_type, list):
            raise RouteException(
                "Method type needs to be a list. Got '{}'".format(method_type)
            )

        # Make all method types in list uppercase
        self.method_type = [x.upper() for x in method_type]
        if route is not None and output is not None:
            self.route(route, output)


class Put(BaseHttpRoute):
    """Class for specifying PUT requests."""

    def __init__(self, route=None, output=None):
        """Put constructor."""
        super().__init__()
        self.method_type = ["PUT"]
        if route is not None and output is not None:
            self.route(route, output)


class Patch(BaseHttpRoute):
    """Class for specifying Patch requests."""

    def __init__(self, route=None, output=None):
        """Patch constructor."""
        super().__init__()
        self.method_type = ["PATCH"]
        if route is not None and output is not None:
            self.route(route, output)


class Delete(BaseHttpRoute):
    """Class for specifying Delete requests."""

    def __init__(self, route=None, output=None):
        """Delete constructor."""
        super().__init__()
        self.method_type = ["DELETE"]
        if route is not None and output is not None:
            self.route(route, output)


class Connect(BaseHttpRoute):
    """Class for specifying Connect requests."""

    def __init__(self, route=None, output=None):
        """Connect constructor."""
        super().__init__()
        self.method_type = ["CONNECT"]
        if route is not None and output is not None:
            self.route(route, output)


class Options(BaseHttpRoute):
    """Class for specifying Options requests."""

    def __init__(self, route=None, output=None):
        """Options constructor."""
        super().__init__()
        self.method_type = ["OPTIONS"]
        if route is not None and output is not None:
            self.route(route, output)

        print(
            "The Masonite development server is not capable of handling OPTIONS preflight requests."
        )
        print("You should use a more powerful server if using the Option")


class Trace(BaseHttpRoute):
    """Class for specifying Trace requests."""

    def __init__(self, route=None, output=None):
        """Trace constructor."""
        super().__init__()
        self.method_type = ["TRACE"]
        if route is not None and output is not None:
            self.route(route, output)


class ViewRoute(BaseHttpRoute):
    def __init__(self, method_type, route, template, dictionary):
        """Class used for view routes.

        This class should be returned when a view is called on an HTTP route.
        This is useful when returning a view that doesn't need any special logic and only needs a dictionary.

        Arguments:
            method_type {string} -- The method type (GET, POST, PUT etc)
            route {string} -- The current route (/test/url)
            template {string} -- The template to use (dashboard/user)
            dictionary {dict} -- The dictionary to use to render the template.
        """

        super().__init__()
        self.method_type = method_type
        self.route_url = route
        self.template = template
        self.dictionary = dictionary
        self._compiled_url = self.compile_route_to_regex()

    def get_response(self):
        return (
            self.request.app()
            .make("ViewClass")
            .render(self.template, self.dictionary)
            .rendered_template
        )


class Redirect(BaseHttpRoute):
    def __init__(self, current_route, future_route, status=302, methods=["GET"]):
        """Class used for view routes.

        This class should be returned when a view is called on an HTTP route.
        This is useful when returning a view that doesn't need any special logic and only needs a dictionary.

        Arguments:
            method_type {string} -- The method type (GET, POST, PUT etc)
            route {string} -- The current route (/test/url)
            template {string} -- The template to use (dashboard/user)
            dictionary {dict} -- The dictionary to use to render the template.
        """
        super().__init__()
        self.method_type = methods
        self.route_url = current_route
        self.status = status
        self.future_route = future_route
        self._compiled_url = self.compile_route_to_regex()

    def get_response(self):
        return self.request.redirect(self.future_route, status=self.status)


class RouteGroup:
    """Class for specifying Route Groups."""

    def __new__(
        cls,
        routes=[],
        middleware=[],
        domain=[],
        prefix="",
        name="",
        add_methods=[],
        namespace="",
    ):
        """Call when this class is first called. This is to give the ability to return a value in the constructor.

        Keyword Arguments:
            routes {list} -- List of routes. (default: {[]})
            middleware {list} -- List of middleware. (default: {[]})
            domain {list} -- String or list of domains to attach to all the routes. (default: {[]})
            prefix {str} -- Prefix to attach to all the route URI's. (default: {''})
            name {str} -- Base name to attach to all the routes. (default: {''})
            namespace {str} -- Namespace path to attach to all the routes. (default: {''})

        Returns:
            list -- Returns a list of routes.
        """
        from .helpers.routes import flatten_routes

        cls.routes = flatten_routes(routes)

        if middleware:
            cls._middleware(cls, *middleware)

        if add_methods:
            cls._add_methods(cls, *add_methods)

        if domain:
            cls._domain(cls, domain)

        if namespace:
            cls._namespace(cls, namespace)

        if prefix:
            cls._prefix(cls, prefix)

        if name:
            cls._name(cls, name)

        return cls.routes

    def _middleware(self, *middleware):
        """Attach middleware to all routes.

        Returns:
            list -- Returns list of routes.
        """
        for route in self.routes:
            route.middleware(*middleware)

        return self.routes

    def _add_methods(self, *methods):
        """Attach more methods to all routes.

        Returns:
            list -- Returns list of routes.
        """
        for route in self.routes:
            route.method_type.append(*methods)

        return self.routes

    def _domain(self, domain):
        """Attach a domain to all routes.

        Arguments:
            domain {str|list|tuple} -- List of domains to attach to all the routes.
        """
        for route in self.routes:
            route.domain(domain)

    def _prefix(self, prefix):
        """Prefix a string to all domain URI's.

        Arguments:
            prefix {str} -- String to prefix to all Routes.
        """
        for route in self.routes:
            if route.route_url == "/":
                route.route_url = ""

            route.route_url = prefix + route.route_url
            route.compile_route_to_regex()

    def _name(self, name):
        """Name to prefix to all routes.

        Arguments:
            name {str} -- String to prefix to all routes.
        """
        for route in self.routes:
            if isinstance(route.named_route, str):
                route.named_route = name + route.named_route

    def _namespace(self, namespace):
        """Namespace of the controller for all routes

        Arguments:
            namespace {str} -- String to add to find controllers for all Routes.
        """
        if not namespace.endswith("."):
            namespace += "."
        for route in self.routes:
            if isinstance(route.output, str):
                route.e = False  # reset any previous find_controller attempt
                route.output = namespace + route.output
                route._find_controller(route.output)


class Resource:
    def __new__(
        cls,
        base="",
        controller="",
        only=["index", "create", "store", "show", "edit", "update", "destroy"],
        names={},
    ):
        routes = []

        if "index" in only:
            route = Get("{}".format(base), "{}@index".format(controller))
            if "index" in names:
                route.name(names["index"])
            routes.append(route)
        if "create" in only:
            route = Get("{}/create".format(base), "{}@create".format(controller))
            if "create" in names:
                route.name(names["create"])
            routes.append(route)
        if "store" in only:
            route = Post("{}".format(base), "{}@store".format(controller))
            if "store" in names:
                route.name(names["store"])
            routes.append(route)
        if "show" in only:
            route = Get("{}/@id".format(base), "{}@show".format(controller))
            if "show" in names:
                route.name(names["show"])
            routes.append(route)
        if "edit" in only:
            route = Get("{}/@id/edit".format(base), "{}@edit".format(controller))
            if "edit" in names:
                route.name(names["edit"])
            routes.append(route)
        if "update" in only:
            route = Match(["PUT", "PATCH"]).route(
                "{}/@id".format(base), "{}@update".format(controller)
            )
            if "update" in names:
                route.name(names["update"])
            routes.append(route)
        if "destroy" in only:
            route = Delete("{}/@id".format(base), "{}@destroy".format(controller))
            if "destroy" in names:
                route.name(names["destroy"])
            routes.append(route)

        return routes

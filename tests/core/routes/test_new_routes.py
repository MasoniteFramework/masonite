from unittest import TestCase
import re
from src.masonite.exceptions import InvalidRouteCompileException, RouteMiddlewareNotFound

class HTTPRoute:

    def __init__(self, url, controller=None, request_method=["get"], name=None):
        self.url = url
        self.controller = controller
        self._name = name
        self.request_method = [x.lower() for x in request_method]
        self.list_middleware = []
        self.compile_route_to_regex()

    def match(self, path, request_method):
        return (re.match(self._compiled_regex, path) or re.match(self._compiled_regex_end, path) and request_method.lower() in self.request_method)

    def match_name(self, name):
        return name == self._name

    def name(self, name):
        self._name = name
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
        split_given_route = self.url.split("/")
        # compile the provided url into regex
        url_list = []
        regex = "^"
        for regex_route in split_given_route:
            if "@" in regex_route:
                if ":" in regex_route:
                    try:
                        regex += Route.compilers[regex_route.split(":")[1]]
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
                    regex += Route.compilers["default"]

                regex += r"\/"

                # append the variable name passed @(variable):int to a list
                url_list.append(regex_route.replace("@", "").split(":")[0])
            elif "?" in regex_route:
                # Make the preceding token match 0 or more
                regex += "?"

                if ":" in regex_route:

                    try:
                        regex += Route.compilers[regex_route.split(":")[1]] + "*"
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
                    regex += Route.compilers["default"] + "*"

                regex += r"\/"

                url_list.append(regex_route.replace("?", "").split(":")[0])
            else:
                regex += regex_route + r"\/"

        self.url_list = url_list
        regex += "$"
        self._compiled_regex = re.compile(regex.replace(r"\/$", r"$"))
        self._compiled_regex_end = re.compile(regex)

        return regex

class Route:
    
    routes = []
    compilers = {
        "int": r"(\d+)",
        "integer": r"(\d+)",
        "string": r"([a-zA-Z]+)",
        "default": r"([\w.-]+)",
        "signed": r"([\w\-=]+)",
    }

    def __init__(self):
        pass

    @classmethod
    def add(self, route):
        self.routes.append(route)
        return self

    @classmethod
    def get(self, url, controller, **options):
        route = HTTPRoute(url, controller, request_method=["get"], **options)
        self.routes.append(route)
        return route

    @classmethod
    def post(self, url, controller, **options):
        route = HTTPRoute(url, controller, request_method=["post"], **options)
        self.routes.append(route)
        return route

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
    def default(self, url, controller, **options):
        self.routes.append(HTTPRoute(url, controller, request_method=["post"], **options))
        return self

    @classmethod
    def match(self, url, controller, **options):
        self.routes.append(HTTPRoute(url, controller, request_method=["post"], **options))
        return self

    @classmethod
    def group(self, *routes, **options):
        for route in routes:
            if options.get('prefix'):
                route.url = options.get('prefix') + route.url
                route.compile_route_to_regex()

            if options.get('name'):
                route._name = options.get('name') + route._name

            self.routes.append(route)
        return self

    def find(self, path, request_method):
        for route in self.routes:
            if route.match(path, request_method):
                return route

    def find_by_name(self, name):
        for route in self.routes:
            if route.match_name(name):
                return route

    @classmethod
    def compile(self, key, to=""):
        self.compilers.update({key: to})
        return self

class TestRoutes(TestCase):

    def test_can_add_routes(self):
        Route.get('/home', 'TestController')
        Route.post('/login', 'TestController')
        self.assertEqual(len(Route().routes), 2)
        
    def test_can_find_route(self):
        Route.get('/home', 'TestController')

        route = Route().find("/home/", "GET")
        self.assertTrue(route)

        route = Route().find("/home", "GET")
        self.assertTrue(route)

    def test_can_find_route_with_parameter(self):
        Route.get('/home/@id', 'TestController')

        route = Route().find("/home/1", "GET")
        self.assertTrue(route)

    def test_can_find_route_optional_params(self):
        Route.get('/home/?id', 'TestController')

        route = Route().find("/home/1", "GET")
        self.assertTrue(route)
        route = Route().find("/home", "GET")
        self.assertTrue(route)

    def test_can_find_route_compiler(self):
        Route.get('/route/@id:int', 'TestController')

        route = Route().find("/route/1", "GET")
        self.assertTrue(route)
        route = Route().find("/route/string", "GET")
        self.assertFalse(route)

    def test_can_make_route_group(self):
        Route.group(
            Route.get('/group', 'TestController@show'),
            Route.post('/login', 'TestController@show'),
            prefix="/testing"
        )

        route = Route().find("/testing/group", "GET")
        self.assertTrue(route)

    def test_group_naming(self):
        Route.group(
            Route.get('/group', 'TestController@show').name(".index"),
            Route.post('/login', 'TestController@show').name(".index"),
            prefix="/testing",
            name="dashboard"
        )

        route = Route().find_by_name("dashboard.index")
        self.assertTrue(route)

    def test_compile_year(self):
        Route.compile('year', r'[0-9]{4}')
        Route.get('/year/@date:year', 'TestController@show')

        route = Route().find("/year/2005", "GET")
        self.assertTrue(route)

    def test_find_by_name(self):
        Route.get('/getname', 'TestController@show').name("testname")

        route = Route().find_by_name("testname")
        self.assertTrue(route)


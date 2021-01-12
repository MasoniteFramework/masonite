from unittest import TestCase
import re

class HTTPRoute:

    def __init__(self, url, controller=None, request_method=["get"]):
        self.url = url
        self.controller = controller
        # self.request_method = request_method
        self.request_method = [x.lower() for x in request_method]
        self.compile_route_to_regex()

    def match(self, path, request_method):
        return ( (re.match(self._compiled_regex, path) or re.match(self._compiled_regex_end, path)) and request_method.lower() in self.request_method)

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
            self.routes.append(route)
        return self

    def find(self, path, request_method):
        for route in self.routes:
            if route.match(path, request_method):
                return route

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


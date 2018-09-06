""" A RouteProvider Service Provider """

import json
import re

from masonite.provider import ServiceProvider
from masonite.view import View
from masonite.request import Request
from masonite.routes import Route


class RouteProvider(ServiceProvider):

    def register(self):
        pass

    def boot(self, router: Route, request: Request):

        # All routes joined
        for route in self.app.make('WebRoutes'):

            """
            |--------------------------------------------------------------------------
            | Make a better match for trailing slashes
            |--------------------------------------------------------------------------
            |
            | Sometimes a user will end with a trailing slash. Because the user might
            | create routes like `/url/route` and `/url/route/` and how the regex
            | is compiled down, we may need to adjust for urls that end or dont
            | end with a trailing slash.
            |
            """

            matchurl = self.create_matchurl(router, route)

            """
            |--------------------------------------------------------------------------
            | Houston, we've got a match
            |--------------------------------------------------------------------------
            |
            | Check to see if a route matches the corresponding router url. If a match
            | is found, execute that route and break out of the loop. We only need
            | one match. Routes are executed on a first come, first serve basis
            |
            """

            if matchurl.match(router.url) and route.method_type == self.app.make('Environ')['REQUEST_METHOD']:
                route.load_request(request)
                if request.has_subdomain():
                    # check if the subdomain matches the routes domain
                    if not route.has_required_domain():
                        self.app.bind('Response', 'Route not found. Error 404')
                        continue

                """
                |--------------------------------------------------------------------------
                | Get URL Parameters
                |--------------------------------------------------------------------------
                |
                | This will create a dictionary of parameters given. This is sort of a short
                | but complex way to retrieve the url parameters. 
                | This is the code used to convert /url/@firstname/@lastname 
                | to {'firstmane': 'joseph', 'lastname': 'mancuso'}.
                |
                """

                try:
                    parameter_dict = {}
                    for index, value in enumerate(matchurl.match(router.url).groups()):
                        parameter_dict[router.generated_url_list()[
                            index]] = value
                    request.set_params(parameter_dict)
                except AttributeError:
                    pass

                """
                |--------------------------------------------------------------------------
                | Execute Before Middleware
                |--------------------------------------------------------------------------
                |
                | This is middleware that contains a before method.
                |
                """

                # Loads the request in so the middleware
                # specified is able to use the
                # request object.
                route.run_middleware('before')

                for http_middleware in self.app.make('HttpMiddleware'):
                    located_middleware = self.app.resolve(
                        http_middleware
                    )
                    if hasattr(located_middleware, 'before'):
                        located_middleware.before()

                """
                |--------------------------------------------------------------------------
                | Get Route Data
                |--------------------------------------------------------------------------
                """

                # Show a helper in the terminal of which route has been visited

                if self.app.make('Application').DEBUG:
                    print(route.method_type + ' Route: ' + router.url)

                # Get the data from the route. This data is typically the
                # output of the controller method
                if not request.redirect_url:
                    request.status('200 OK')

                    response = route.get_response()

                    self.app.bind(
                        'Response',
                        router.get(route.route, response)
                    )

                """
                |--------------------------------------------------------------------------
                | Execute After Middleware
                |--------------------------------------------------------------------------
                |
                | This is middleware with an after method.
                |
                """

                # Loads the request in so the middleware
                # specified is able to use the
                # request object.
                route.run_middleware('after')

                for http_middleware in self.app.make('HttpMiddleware'):
                    located_middleware = self.app.resolve(
                        http_middleware
                    )
                    if hasattr(located_middleware, 'after'):
                        located_middleware.after()

                # Breaks the loop because the incoming route is found and executed.
                # There is no need to continue searching WebRoutes.
                break
            else:
                self.app.bind('Response', 'Route not found. Error 404')

    def create_matchurl(self, router, route):
        """Creates a regex string for router.url to be matched against

        Arguments:
            router {masonite.routes.Route} -- The Masonite route object
            route {masonite.routes.BaseHttpRoute} -- The current route being executed.

        Returns:
            string -- compiled regex string
        """

        # Compiles the given route to regex
        regex = router.compile_route_to_regex(route)

        if route.route_url.endswith('/'):
            matchurl = re.compile(regex.replace(r'\/\/$', r'\/$'))
        else:
            matchurl = re.compile(regex.replace(r'\/$', r'$'))

        return matchurl

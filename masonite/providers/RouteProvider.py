"""A RouteProvider Service Provider."""

from masonite.provider import ServiceProvider
from masonite.request import Request
from masonite.routes import Route
from masonite.helpers.routes import create_matchurl
from config import application


class RouteProvider(ServiceProvider):

    def register(self):
        pass

    def boot(self, router: Route, request: Request):
        # All routes joined
        for route in self.app.make('WebRoutes'):

            """Make a better match for trailing slashes
            Sometimes a user will end with a trailing slash. Because the user might
            create routes like `/url/route` and `/url/route/` and how the regex
            is compiled down, we may need to adjust for urls that end or dont
            end with a trailing slash.
            """

            matchurl = create_matchurl(router, route)

            """Houston, we've got a match
                Check to see if a route matches the corresponding router url. If a match
                is found, execute that route and break out of the loop. We only need
                one match. Routes are executed on a first come, first serve basis
            """

            if matchurl.match(router.url) and request.get_request_method() in route.method_type:
                route.load_request(request)
                if request.has_subdomain():
                    # Check if the subdomain matches the routes domain
                    if not route.has_required_domain():
                        self.app.bind('Response', 'Route not found. Error 404')
                        continue

                """Get URL Parameters
                    This will create a dictionary of parameters given. This is sort of a short
                    but complex way to retrieve the url parameters.
                    This is the code used to convert /url/@firstname/@lastname
                    to {'firstmane': 'joseph', 'lastname': 'mancuso'}.
                """

                try:
                    parameter_dict = {}
                    for index, value in enumerate(matchurl.match(router.url).groups()):
                        parameter_dict[router.generated_url_list()[index]] = value
                    request.set_params(parameter_dict)
                except AttributeError:
                    pass

                """Excute HTTP before middleware
                    Only those middleware that have a "before" method are ran.
                """

                for http_middleware in self.app.make('HttpMiddleware'):
                    located_middleware = self.app.resolve(
                        http_middleware
                    )
                    if hasattr(located_middleware, 'before'):
                        located_middleware.before()

                """Execute Before Middleware
                    This is middleware that contains a before method.
                """

                route.run_middleware('before')

                # Show a helper in the terminal of which route has been visited
                if application.DEBUG:
                    print(request.get_request_method() + ' Route: ' + router.url)

                if request.get_status_code() == '404 Not Found':
                    request.status(200)

                    # Get the response from the route. This data is typically the
                    # output of the controller method
                    self.app.bind(
                        'Response',
                        route.get_response()
                    )

                """Execute After Route Middleware
                    This is middleware that contains an after method.
                """

                route.run_middleware('after')

                """Excute HTTP after middleware
                    Only those middleware that have an "after" method are ran.
                """

                for http_middleware in self.app.make('HttpMiddleware'):
                    located_middleware = self.app.resolve(
                        http_middleware
                    )
                    if hasattr(located_middleware, 'after'):
                        located_middleware.after()

                # Breaks the loop because the incoming route is found and executed.
                # There is no need to continue searching the route list.
                break
            else:
                self.app.bind('Response', 'Route not found. Error 404')

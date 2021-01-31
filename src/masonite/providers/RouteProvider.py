"""A RouteProvider Service Provider."""

from ..helpers.routes import create_matchurl
from ..provider import ServiceProvider
from ..request import Request
from ..response import Response
from ..routes import Route


class RouteProvider(ServiceProvider):
    def register(self):
        pass

    def boot(self, router: Route, request: Request, response: Response):
        # All routes joined
        from config import application

        route = router.find(request.path, request.get_request_method())

        if route:
            request.set_params(route.extract_parameters(request.path))

            for http_middleware in self.app.make("HttpMiddleware"):
                located_middleware = self.app.resolve(http_middleware)
                if hasattr(located_middleware, "before"):
                    located_middleware.before()

            route.run_middleware("before")

            if application.DEBUG:
                # TODO: Extract this out to logging method
                print(request.get_request_method() + " Route: " + request.path)

            if not response.get_status_code():

                """Get the response from the route and set it on the 'Response' key.
                This data is typically the output of the controller method depending
                on the type of route.
                """
                response.view(route.get_response(self.app), status=200)

            route.run_middleware("after")

            for http_middleware in self.app.make("HttpMiddleware"):
                located_middleware = self.app.resolve(http_middleware)

                if hasattr(located_middleware, "after"):
                    located_middleware.after()
        else:
            """No Response was found in the for loop so let's set an arbitrary response now."""
            # If the route exists but not the method is incorrect
            if router.matches(request.path):
                response.view("Method not allowed", status=405)
            else:
                response.view("Not Found", status=404)

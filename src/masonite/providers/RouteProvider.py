from inspect import isclass

from ..facades import Response as ResponseFacade
from .Provider import Provider
from ..routes import Route
from ..routes.commands import RouteListCommand
from ..pipeline import Pipeline
from ..exceptions import RouteNotFoundException, MethodNotAllowedException


class RouteProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        Route.set_controller_locations(self.application.make("controllers.location"))
        self.application.make("commands").add(RouteListCommand(self.application))

    def boot(self):
        from ..response import Response

        router = self.application.make("router")
        request = self.application.make("request")
        response = self.application.make("response")

        route = router.find(
            request.get_path(), request.get_request_method(), request.get_subdomain()
        )
        if not route:
            raise RouteNotFoundException(
                f"{request.get_request_method()} {request.get_path()} : 404 Not Found"
            )

        request.route = route

        # Run before middleware
        before_middleware = Pipeline(request, response).through(
            self.application.make("middleware").get_http_middleware(),
            handler="before",
        )

        exception = None
        if before_middleware:
            request.load_params(route.extract_parameters(request.get_path()))
            route_middleware = self.application.make("middleware").run_route_middleware(
                route.get_middlewares(), request, response, callback="before"
            )

            if route_middleware:
                try:
                    data = route.get_response(self.application)
                    if isinstance(data, Response) or (
                        isclass(data) and issubclass(data, ResponseFacade)
                    ):
                        pass
                    else:
                        response.view(data)
                except Exception as e:
                    if not response.get_status_code():
                        response.status(500)
                    exception = e

                self.application.make("middleware").run_route_middleware(
                    route.get_middlewares(), request, response, callback="after"
                )

        Pipeline(request, response).through(
            self.application.make("middleware").get_http_middleware(),
            handler="after",
        )

        if exception:
            raise exception

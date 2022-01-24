"""Route List Command"""
import re
from cleo import Command


class RouteListCommand(Command):
    """
    List all your application routes.

    routes:list
        {--M|methods= : Filter by a list of HTTP methods: GET or GET,POST}
        {--N|name= : Filter by route name}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        # get filters
        methods = self.option("methods")
        if methods:
            methods = list(map(lambda m: m.lower(), methods.split(",")))
        name = self.option("name")

        # get routes
        router = self.app.make("router")
        routes = router.routes

        # filter by HTTP methods
        if methods:
            routes = list(
                filter(
                    lambda route: set(route.request_method).intersection(methods),
                    routes,
                )
            )
        # filter by name
        if name:
            routes = list(
                filter(
                    lambda route: re.findall(
                        name, route.get_name() or "", re.IGNORECASE
                    ),
                    routes,
                )
            )

        # build routes table
        header = ["URI", "Name", "Method(s)", "Controller", "Middleware(s)"]
        rows = list(map(lambda route: self.format_route_as_row(route), routes))
        rows.sort()
        self.render_table(header, rows)

    def format_route_as_row(self, route):
        """Format a Route object as a table row."""
        # format controller name
        if callable(route.controller):
            # ControllerClassName.index -> ControllerClassName@index
            controller = route.controller.__qualname__.replace(".", "@")
        else:
            controller = str(route.controller)
        row = [
            route.url,
            route.get_name() or "",
            "/".join(map(lambda m: m.upper(), route.request_method)),
            controller,
            ",".join(route.get_middlewares()),
        ]
        return row

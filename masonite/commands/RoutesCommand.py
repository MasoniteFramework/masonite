
from cleo import Command
from tabulate import tabulate


class RoutesCommand(Command):
    """
    List out all routes of the application.

    show:routes
    """

    def handle(self):
        from wsgi import container

        web_routes = container.make('WebRoutes')

        routes = [[
            "Method",
            "Path",
            "Name",
            "Domain",
            "Middleware"
        ]]

        for route in web_routes:
            routes.append([
                route.method_type,
                route.route_url,
                route.named_route,
                route.required_domain,
                ','.join(route.list_middleware),
            ])

        print(tabulate(routes, headers="firstrow", tablefmt="rst"))

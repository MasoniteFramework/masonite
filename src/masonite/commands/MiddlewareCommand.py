"""New Middleware Command."""
from ..commands import BaseScaffoldCommand


class MiddlewareCommand(BaseScaffoldCommand):
    """
    Creates a middleware.

    middleware
        {name : Name of the middleware}
    """

    scaffold_name = "Middleware"
    suffix = "Middleware"
    template = "/masonite/snippets/scaffold/middleware"
    base_directory = "app/http/middleware/"

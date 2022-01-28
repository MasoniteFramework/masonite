from .. import Middleware


class ClearDumpsBetweenRequestsMiddleware(Middleware):
    """Clear dumps between each requests to avoid showing too much data."""

    def before(self, request, response):
        request.app.make("dumper").clear()
        return request

    def after(self, request, response):
        return request

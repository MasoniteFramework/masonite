""" CORS Middleware """

from masonite.request import Request


class CORSMiddleware:
    """CORS Middleware
    |--------------------------------------------------------------------------
    | Create Dictionary of CORS headers
    |--------------------------------------------------------------------------
    |
    | Appends CORS headers to HTTP response
    |
    | Ex. cors = {"Access-Control-Allow-Origin": "*",
    |             "Access-Control-Allow-Headers": "Content-Type",
    |             "Access-Control-Allow-Methods": "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT"}
    |
    """

    CORS = {}

    def __init__(self, request: Request):
        """Inject Any Dependencies From The Service Container

        Arguments:
            Request {masonite.request.Request} -- The Masonite request object
        """
        self.request = request

    def after(self):
        """Run This Middleware After The Route Executes
        """
        for key, value in self.CORS.items():
            self.request.header(key, value, http_prefix=None)

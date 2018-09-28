""" CORS Middleware """
from masonite.request import Request


class CorsMiddleware:

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT"
    }

    def __init__(self, request: Request):
        self.request = request

    def before(self):
        self.request.header(self.headers)

import os
import sys
from http.request import Request
from http.routes import Route
import importlib


def app(environ, start_response):
        os.environ.setdefault('REQUEST_METHOD', environ['REQUEST_METHOD'])
        os.environ.setdefault('URI_PATH', environ['PATH_INFO'])
        # print(environ)
        router = Route(environ)
        # routes = [route.get('/uouo', lambda: 'mario'), route.get('/boo', 'im a ghost')]

        routes = importlib.import_module('views.view').routes

        for route in routes:
            print(route.route)
            if route.route == router.url:
                data = router.get(route.route, route.output)
                break
            else:
                data = 'Route not found'

        data = bytes(data)
        # data = bytes(route.get(environ['PATH_INFO']))

        start_response("200 OK", [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(data)))
        ])
        return iter([data])

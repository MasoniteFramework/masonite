import os
import importlib
from app.http.providers.routes import Route
from config import app

def app(environ, start_response):
    os.environ.setdefault('REQUEST_METHOD', environ['REQUEST_METHOD'])
    os.environ.setdefault('URI_PATH', environ['PATH_INFO'])
    router = Route(environ)

    routes = importlib.import_module('routes.web').routes

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

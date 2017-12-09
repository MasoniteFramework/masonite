import os
from app.http.providers.routes import Route
from app.http.providers.request import Request
from dotenv import load_dotenv, find_dotenv

# load all .env information into environment
load_dotenv(find_dotenv())

def app(environ, start_response):
    ''' Framework Engine '''
    os.environ.setdefault('REQUEST_METHOD', environ['REQUEST_METHOD'])
    os.environ.setdefault('URI_PATH', environ['PATH_INFO'])

    # if this is a post request
    if environ['REQUEST_METHOD'] == 'POST':
        l = int(environ.get('CONTENT_LENGTH')) if environ.get(
            'CONTENT_LENGTH') else 0
        body = environ['wsgi.input'].read(l) if l > 0 else ''
        environ['QUERY_STRING'] = body

    router = Route(environ)
    import routes.web
    routes = routes.web.routes

    for route in routes:
        if route.route == router.url:
            data = router.get(route.route, route.output(Request(environ)))
            break
        else:
            data = 'Route not found'

    data = bytes(data)

    start_response("200 OK", [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])

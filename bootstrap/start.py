''' Start of Application. This function is the gunicorn server '''

import os
import re


from dotenv import find_dotenv, load_dotenv
from masonite.request import Request
from masonite.routes import Route
from masonite.storage import Storage

# Load environment variable from .env file
load_dotenv(find_dotenv())

# Run once and only once the server is ran
Storage().compile_sass()

def app(environ, start_response):
    ''' Framework Engine '''
    os.environ.setdefault('REQUEST_METHOD', environ['REQUEST_METHOD'])
    os.environ.setdefault('URI_PATH', environ['PATH_INFO'])

    # if this is a post request
    router = Route(environ)

    if router.is_post():
        # Set POST parameters given into the query string to centralize parsing and retrieval.
        environ['QUERY_STRING'] = router.set_post_params()

    # Get all routes from the routes/web.py file
    import routes.web
    routes = routes.web.ROUTES

    # Instantiate the Request object
    request = Request(environ)

    # Check all http routes
    for route in routes:
        # Compiles the given route to regex
        regex = router.compile_route_to_regex(route)

        # Make a better match trailing slashes `/` at the end of routes
        if route.route_url.endswith('/'):
            matchurl = re.compile(regex.replace(r'\/\/$', r'\/$'))
        else:
            matchurl = re.compile(regex.replace(r'\/$', r'$'))

        try:
            parameter_dict = {}
            for index, value in enumerate(matchurl.match(router.url).groups()):
                parameter_dict[router.generated_url_list()[index]] = value
            request.set_params(parameter_dict)
        except AttributeError:
            pass

        if matchurl.match(router.url) and route.method_type == environ['REQUEST_METHOD'] and route.continueroute is True:
            print(route.method_type + ' Route: ' + router.url)
            data = router.get(route.route, route.output(request))
            break
        else:
            data = 'Route not found. Error 404'

    ## Check all API Routes
    if data == 'Route not found. Error 404':
        # look at the API routes files
        import routes.api
        routes = routes.api.ROUTES

        for route in routes:
            if route.url in router.url:
                data = route.fetch(request).output
                if data:
                    break
                else:
                    data = 'Route not found. Error 404'
            else:
                data = 'Route not found. Error 404'

    ## Set redirection if a route has been called to redirect to
    if request.redirect_route:
        for route in routes:
            if route.named_route == request.redirect_route:
                print(route.method_type + ' Named Route: ' + router.url)
                data = router.get(route.route, route.output(request))
                request.redirect_url = route.route_url


    data = bytes(data, 'utf-8')


    if not request.redirect_url:
        # Normal HTTP response
        start_response("200 OK", [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(data)))
        ] + request.get_cookies())
    else:
        # Redirection
        start_response("302 OK", [
            ('Location', request.redirect_url)
        ] + request.get_cookies())

    return iter([data])

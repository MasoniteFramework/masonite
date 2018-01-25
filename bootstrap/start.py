''' Start of Application. This function is the gunicorn server '''
import os
import re

from dotenv import find_dotenv, load_dotenv
from masonite.request import Request
from masonite.routes import Route
from masonite.storage import Storage
from config import middleware
from pydoc import locate

# Load environment variable from .env file
load_dotenv(find_dotenv())

# Run once and only once the server is ran
# This will not actually compile if the libsass module in not installed
Storage().compile_sass()

def app(environ, start_response):
    ''' Framework Engine '''
    os.environ.setdefault('REQUEST_METHOD', environ['REQUEST_METHOD'])
    os.environ.setdefault('URI_PATH', environ['PATH_INFO'])

    router = Route(environ)

    if router.is_post():
        # Set POST parameters given into the query string to centralize parsing and retrieval.
        # This was made to directly support the Request.input() method.
        # There is no known reason to differentiate between GET and POST when retrieving
        #    form paramters. This line below simply puts both POST form params in the
        #    same query_string as GET params.
        environ['QUERY_STRING'] = router.set_post_params()

    # Get all routes from the routes/web.py file
    import routes.web
    routes = routes.web.ROUTES

    # Instantiate the Request object.
    # This is the `request` object passed into controller methods
    request = Request(environ)

    # Check all http routes
    for route in routes:
        # Compiles the given route to regex
        regex = router.compile_route_to_regex(route)

        # Make a better match trailing slashes `/` at the end of routes
        # Sometimes a user will end with a trailing slash. Because the
        #    user may create routes like `/url/route` and `/url/route/`
        #    and how the regex is compiled down, we may need to adjust for
        #    urls that end or dont end with a trailing slash. This is sort
        #    of a quirk and could possibly be fixed.
        if route.route_url.endswith('/'):
            matchurl = re.compile(regex.replace(r'\/\/$', r'\/$'))
        else:
            matchurl = re.compile(regex.replace(r'\/$', r'$'))

        # This will create a dictionary of paramters given. This is a sort of a short
        #     but complex way to retrieve the url paramters. This is the code used to
        #     convert /url/@firstname/@lastname to {'firstmane': 'joseph', 'lastname': 'mancuso'}
        try:
            parameter_dict = {}
            for index, value in enumerate(matchurl.match(router.url).groups()):
                parameter_dict[router.generated_url_list()[index]] = value
            request.set_params(parameter_dict)
        except AttributeError:
            pass

        # If the route url matches the regex and the method type and the route can continue
        #     (will be used with middleware later)
        if matchurl.match(router.url) and route.method_type == environ['REQUEST_METHOD'] and route.continueroute is True:

            # Execute HTTP Before Middleware
            for http_middleware in middleware.HTTP_MIDDLEWARE:
                located_middleware = locate(http_middleware)
                if hasattr(located_middleware, 'before'):
                    located_middleware(request).before()

            # Show a helper in the terminal of which route has been visited
            print(route.method_type + ' Route: ' + router.url)

            # Loads the request in so the middleware specified is able to use the
            #     request object. This is before middleware and is ran before the request
            route.load_request(request).run_middleware('before')

            # Get the data from the route. This data is typically the output
            #     of the controller method
            if not request.redirect_url:
                data = router.get(route.route, route.output(request))

            # Loads the request in so the middleware specified is able to use the
            #     request object. This is after middleware and is ran after the request
            route.load_request(request).run_middleware('after')

            # Execute HTTP After Middleware
            for http_middleware in middleware.HTTP_MIDDLEWARE:
                located_middleware = locate(http_middleware)
                if hasattr(located_middleware, 'after'):
                    located_middleware(request).after()
            break
        else:
            data = 'Route not found. Error 404'

    ## Check all API Routes
    if data == 'Route not found. Error 404':
        # Look at the API routes files
        import routes.api
        routes = routes.api.ROUTES

        for route in routes:

            # If the base url matches
            if route.url in router.url:
                data = route.fetch(request).output
                if data:
                    break
                else:
                    data = 'Route not found. Error 404'
            else:
                data = 'Route not found. Error 404'

    # Set redirection if a route has been called to redirect to.
    # redirect_route is a property set on the request object when
    #     methods like request.redirectTo('nameRoute') are called
    if request.redirect_route:
        for route in routes:
            if route.named_route == request.redirect_route:
                print(route.method_type + ' Named Route: ' + router.url)
                data = router.get(route.route, route.output(request))
                request.redirect_url = route.route_url

    if not request.redirect_url:
        # Convert the data that is retrieved above to bytes so the wsgi server can handle it.
        data = bytes(data, 'utf-8')

        # Normal HTTP response.
        start_response("200 OK", [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(data)))
        ] + request.get_cookies())
    else:
        data = bytes('redirecting ..', 'utf-8')
        # Redirection. In order to redirect the response types need to be 302 instead of 200
        start_response("302 OK", [
            ('Location', request.compile_route_to_url())
        ] + request.get_cookies())

    # This will output the data to the browser.
    return iter([data])

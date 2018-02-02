''' Start of Application. This function is the gunicorn server '''
import os
import re

# Load environment variable from .env file
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from masonite.storage import Storage
from masonite.app import App
from config import application
from pydoc import locate

'''
|--------------------------------------------------------------------------
| Compile Sass
|--------------------------------------------------------------------------
|
| Compile Sass if the libsass module is installed. Once installed, all
| Sass files are compiled when the server is ran. This will only run
| once when the server is first started.
|
'''

Storage().compile_sass()

def app(environ, start_response):
    ''' Framework Engine '''
    
    '''
    |--------------------------------------------------------------------------
    | Startup the Service Container
    |--------------------------------------------------------------------------
    |
    | Instantiate the Service Container so we can bind classes into it and 
    | bind the environ variable that is created by the WSGI server into
    | the container.
    |
    '''

    app = App()
    app.bind('Environ', environ)
    
    '''
    |--------------------------------------------------------------------------
    | Execute All Service Providers
    |--------------------------------------------------------------------------
    |
    | Run all service providers register and boot methods to load objects into
    | the container. Ensure that the providers register methods are executed
    | first, and then run through the list and execute the boot methods.
    | This ensures that the boot method has access to methods in the
    | container.
    |
    '''

    for provider in application.PROVIDERS:
        locate(provider)().load_app(app).register()

    for provider in application.PROVIDERS:
        app.resolve(locate(provider)().load_app(app).boot)

    request = app.make('Request')
    router = app.make('Route')

    '''
    |--------------------------------------------------------------------------
    | Run Through All Http Routes
    |--------------------------------------------------------------------------
    |
    | Retrieve and loop through the web routes from the Service Container.
    |
    '''

    for route in app.make('WebRoutes'):
        # Compiles the given route to regex
        regex = router.compile_route_to_regex(route)

        '''
        |--------------------------------------------------------------------------
        | Make a better match for trailing slashes
        |--------------------------------------------------------------------------
        |
        | Sometimes a user will end with a trailing slash. Because the user might
        | create routes like `/url/route` and `/url/route/` and how the regex 
        | is compiled down, we may need to adjust for urls that end or dont 
        | end with a trailing slash.
        |
        '''
        
        if route.route_url.endswith('/'):
            matchurl = re.compile(regex.replace(r'\/\/$', r'\/$'))
        else:
            matchurl = re.compile(regex.replace(r'\/$', r'$'))

        # This will create a dictionary of parameters given. This is sort of a short
        #     but complex way to retrieve the url parameters. This is the code used to
        #     convert /url/@firstname/@lastname to {'firstmane': 'joseph', 'lastname': 'mancuso'}
        try:
            parameter_dict = {}
            for index, value in enumerate(matchurl.match(router.url).groups()):
                parameter_dict[router.generated_url_list()[index]] = value
            request.set_params(parameter_dict)
        except AttributeError:
            pass

        '''
        |--------------------------------------------------------------------------
        | Houston, we've got a match
        |--------------------------------------------------------------------------
        |
        | Check to see if a route matches the corresponding router url. If a match
        | is found, execute that route and break out of the loop. We only need
        | one match. Routes are executed on a first come, first serve basis
        |
        '''

        if matchurl.match(router.url) and route.method_type == environ['REQUEST_METHOD']:

            '''
            |--------------------------------------------------------------------------
            | Execute Before Middleware
            |--------------------------------------------------------------------------
            |
            | This is middleware that contains a before method.
            |
            '''

            for http_middleware in app.make('HttpMiddleware'):
                located_middleware = locate(http_middleware)
                if hasattr(located_middleware, 'before'):
                    app.resolve(located_middleware().before)

            # Show a helper in the terminal of which route has been visited
            print(route.method_type + ' Route: ' + router.url)

            # Loads the request in so the middleware specified is able to use the
            #     request object. This is before middleware and is ran before the request
            route.load_request(request).run_middleware('before')

            # Get the data from the route. This data is typically the output
            #     of the controller method
            if not request.redirect_url:
                data = router.get(route.route, app.resolve(route.output))

            # Loads the request in so the middleware specified is able to use the
            #     request object. This is after middleware and is ran after the request
            route.load_request(request).run_middleware('after')

            '''
            |--------------------------------------------------------------------------
            | Execute After Middleware
            |--------------------------------------------------------------------------
            |
            | This is middleware with an after method.
            |
            '''

            for http_middleware in app.make('HttpMiddleware'):
                located_middleware = locate(http_middleware)
                if hasattr(located_middleware, 'after'):
                    app.resolve(located_middleware().after)
            break
        else:
            data = 'Route not found. Error 404'

    '''
    |--------------------------------------------------------------------------
    | No Matches for Http Routes Were Found
    |--------------------------------------------------------------------------
    |
    | Since, we found no matches, let's look through the Api routes
    |
    '''

    if data == 'Route not found. Error 404':

        '''
        |--------------------------------------------------------------------------
        | Pull in the API Routes from the Service Container
        |--------------------------------------------------------------------------
        |
        | The Service Container has loaded all Api routes into the container so
        | let's loop through and check for any matches.
        |
        '''

        for route in app.make('ApiRoutes'):

            '''
            |--------------------------------------------------------------------------
            | If We've Got A Match
            |--------------------------------------------------------------------------
            |
            | If we have a match then let's go ahead and execute the route, load the 
            | response into the data variable and get on with our lives.
            |
            '''

            if route.url in router.url:
                data = route.fetch(request).output
                if data:
                    break
                else:
                    data = 'Route not found. Error 404'
            else:
                data = 'Route not found. Error 404'

    '''
    |--------------------------------------------------------------------------
    | Redirect To A Named Route
    |--------------------------------------------------------------------------
    |
    | Sometimes we may need to redirect to a named route. Because of this, we
    | will need to loop back through all the routes and find a route with a
    | name that matches the named route we supplied.
    |
    '''
    if request.redirect_route:
        for route in routes:
            if route.named_route == request.redirect_route:
                print(route.method_type + ' Named Route: ' + router.url)
                data = router.get(route.route, route.output(request))
                request.redirect_url = route.route_url

    '''
    |--------------------------------------------------------------------------
    | We Are Ready For Launch
    |--------------------------------------------------------------------------
    |
    | If we have a solid response and not redirecting then we need to return
    | a 200 status code along with the data. If we don't, then we'll have
    | to return a 302 and redirect to where the developer would like to
    | go next.
    |
    '''
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

    '''
    |--------------------------------------------------------------------------
    | Final Step
    |--------------------------------------------------------------------------
    |
    | This will take the data variable from above and return it to the WSGI
    | server.
    |
    '''
    return iter([data])

''' Middleware Configuration Settings '''

'''
|--------------------------------------------------------------------------
| HTTP Middleware
|--------------------------------------------------------------------------
|
| HTTP middleware is middleware that will be ran on every request. Middleware
| is only ran when a HTTP call is successful (a 200 response). This list
| should contain a simple aggregate of middleware classes.
|
'''

HTTP_MIDDLEWARE = [
    'app.http.middleware.LoadUserMiddleware.LoadUserMiddleware',
    'app.http.middleware.CsrfMiddleware.CsrfMiddleware',
]

'''
|--------------------------------------------------------------------------
| Route Middleware
|--------------------------------------------------------------------------
|
| Route middleware is middleware that is registered with a name and can
| be used in the routes/web.py file. This middleware should really be
| used for middleware on an individual route like a dashboard route.
|
| The Route Middleware is a dictionary with the key being what is specified
| in your route/web.py file (in the .middleware() method) and the value is
| a string with the full module path of the middleware class
|
'''

ROUTE_MIDDLEWARE = {
    'auth':  'app.http.middleware.AuthenticationMiddleware.AuthenticationMiddleware',
}

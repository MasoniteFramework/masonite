''' Middleware Configuration File '''

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
    'app.http.middleware.AuthenticationMiddleware.AuthenticationMiddleware'
]

'''
|--------------------------------------------------------------------------
| Route Middleware
|--------------------------------------------------------------------------
|
| Route middleware is middleware that is registered with a name and can
| be used in the routes/web.py file. This middleware should really be
| used for middleware on an individual route like a dashboard route
|
'''

ROUTE_MIDDLEWARE = {
    'auth':  'app.http.middleware.RouteMiddleware.RouteMiddleware',
}

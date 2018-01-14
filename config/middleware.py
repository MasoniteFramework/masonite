from app.http.middleware.AuthenticationMiddleware import AuthenticationMiddleware

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
    AuthenticationMiddleware
]

'''
|--------------------------------------------------------------------------
| Route Middleware
|--------------------------------------------------------------------------
|
| Route middleware is middleware that is registered with a name and can
| be used in the routes/web.py file. This middleware should really be
| used for middleware on an individual request
|
'''

from app.http.middleware.RouteMiddleware import RouteMiddleware

ROUTE_MIDDLEWARE = {
    'auth': RouteMiddleware
}

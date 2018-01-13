from app.http.middleware.AuthenticationMiddleware import AuthenticationMiddleware
from app.http.middleware.RouteMiddleware import RouteMiddleware

HTTP_MIDDLEWARE = [
    AuthenticationMiddleware
]

ROUTE_MIDDLEWARE = {
    'auth': RouteMiddleware
}

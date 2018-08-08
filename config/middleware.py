from app.http.middleware.AuthenticationMiddleware import AuthenticationMiddleware
ROUTE_MIDDLEWARE = {
    'auth': AuthenticationMiddleware
}
HTTP_MIDDLEWARE = {}
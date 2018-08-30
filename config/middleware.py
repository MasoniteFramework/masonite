from app.http.middleware.MiddlewareTest import MiddlewareTest
from app.http.middleware.AuthenticationMiddleware import AuthenticationMiddleware
from masonite.middleware import JsonResponseMiddleware
from app.http.middleware.AddAttributeMiddleware import AddAttributeMiddleware


ROUTE_MIDDLEWARE = {
    'test': MiddlewareTest,
    'auth': AuthenticationMiddleware,
    'middleware.test': [
        MiddlewareTest,
        AddAttributeMiddleware,
    ]
}

HTTP_MIDDLEWARE = [
    JsonResponseMiddleware
]

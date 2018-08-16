from app.http.middleware.MiddlewareTest import MiddlewareTest
from app.http.middleware.AddAttributeMiddleware import AddAttributeMiddleware


ROUTE_MIDDLEWARE = {
    'test': MiddlewareTest,
    'middleware.test': [
        MiddlewareTest,
        AddAttributeMiddleware,
    ]
}

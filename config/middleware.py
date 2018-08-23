ROUTE_MIDDLEWARE = {
    'test': 'app.http.middleware.MiddlewareTest.MiddlewareTest',
    'middleware.test': [
        'app.http.middleware.MiddlewareTest.MiddlewareTest',
        'app.http.middleware.AddAttributeMiddleware.AddAttributeMiddleware'
    ]
}

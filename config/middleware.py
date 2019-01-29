"""Middleware Configuration Settings."""

from masonite.middleware import (MaintenanceModeMiddleware, ResponseMiddleware,
                                 SecureHeadersMiddleware)

from app.http.middleware.AddAttributeMiddleware import AddAttributeMiddleware
from app.http.middleware.AuthenticationMiddleware import \
    AuthenticationMiddleware
from app.http.middleware.CsrfMiddleware import CsrfMiddleware
from app.http.middleware.LoadUserMiddleware import LoadUserMiddleware
from app.http.middleware.MiddlewareTest import MiddlewareTest
from app.http.middleware.VerifyEmailMiddleware import VerifyEmailMiddleware

"""HTTP Middleware
HTTP middleware is middleware that will be ran on every request. Middleware
is only ran when a HTTP call is successful (a 200 response). This list
should contain a simple aggregate of middleware classes.
"""

HTTP_MIDDLEWARE = [
    LoadUserMiddleware,
    # todo
    # CsrfMiddleware,
    ResponseMiddleware,
    MaintenanceModeMiddleware,
    SecureHeadersMiddleware,
]

"""Route Middleware
Specify a dictionary of middleware to be used on a per route basis here. The key will 
be the alias to use on routes and the value can be any middleware class or a list
of middleware (middleware stacks).
"""

ROUTE_MIDDLEWARE = {
    'auth': AuthenticationMiddleware,
    'test': MiddlewareTest,
    'verified': VerifyEmailMiddleware,
    'middleware.test': [
        MiddlewareTest,
        AddAttributeMiddleware,
    ]
}

"""Secure Headers to use in masonite.middlware.SecureHeadersMiddleware"""

SECURE_HEADERS = {
    'Strict-Transport-Security': 'max-age=63072000; includeSubdomains',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'X-Content-Type-Options': 'sniff-test',
    'Referrer-Policy': 'no-referrer, strict-origin-when-cross-origin',
    'Cache-control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
}
"""CSRF Middleware."""

from masonite.middleware import CsrfMiddleware as Middleware


class CsrfMiddleware(Middleware):
    """Verify CSRF Token Middleware."""

    """Which routes should be exempt from CSRF protection."""
    exempt = [
        #
    ]

    """Whether or not the CSRF token should be changed on every request."""
    every_request = False

    """The length of the token to generate."""
    token_length = 30

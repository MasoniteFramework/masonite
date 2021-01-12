"""SecureHeaders Middleware."""

from ..response import Response


class SecureHeadersMiddleware:
    """SecureHeaders Middleware."""

    def __init__(self, response: Response):
        """Inject Any Dependencies From The Service Container.

        Arguments:
            Response {masonite.response.Response} -- The Masonite response object
        """
        self.response = response
        self.headers = {
            "Strict-Transport-Security": "max-age=63072000; includeSubdomains",
            "X-Frame-Options": "SAMEORIGIN",
            "X-XSS-Protection": "1; mode=block",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "no-referrer, strict-origin-when-cross-origin",
            "Cache-control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
        }

    def before(self):
        """Run This Middleware Before The Route Executes."""
        pass

    def after(self):
        """Run This Middleware After The Route Executes."""
        from config import middleware

        try:
            # Try importing secure headers if they exist in the config file
            self.headers.update(middleware.SECURE_HEADERS)
        except AttributeError:
            pass

        self.response.header(self.headers)

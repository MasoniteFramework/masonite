"""Session Cookie Module."""


class CookieDriver:
    """Cookie Session Driver."""

    def __init__(self, application):
        """Cookie Session Constructor.

        Arguments:
            application {dict} -- The application class
        """
        self.application = application

    def start(self):
        request = self.get_request()
        data = {}
        flashed = {}
        for key, value in request.cookie_jar.to_dict().items():
            if key.startswith("s_"):
                data.update({key.replace("s_", ""): value})
            elif key.startswith("f_"):
                flashed.update({key.replace("f_", ""): value})

        return {"data": data, "flashed": flashed}

    def save(self, added=None, deleted=None, flashed=None, deleted_flashed=None):
        response = self.get_response()
        if added is None:
            added = {}
        if deleted is None:
            deleted = []
        if flashed is None:
            flashed = {}
        if deleted_flashed is None:
            deleted_flashed = []

        for key, value in added.items():
            response.cookie(f"s_{key}", value)

        for key, value in flashed.items():
            response.cookie(f"f_{key}", value)

        for key in deleted:
            response.delete_cookie(f"s_{key}")

        for key in deleted_flashed:
            response.delete_cookie(f"f_{key}")

    def get_response(self):
        return self.application.make("response")

    def get_request(self):
        return self.application.make("request")

    def helper(self):
        """Use to create builtin helper function."""
        return self

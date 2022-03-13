class Url:
    """URL helper facade."""

    def url(path: str = "") -> str:
        """Generates a fully qualified url to the given path. If no path is given this will return
        the base url domain."""
        ...
    def asset(alias: str, filename: str) -> str:
        """Generates a fully qualified URL for the given asset using the given disk
        Example:
            asset("local", "avatar.jpg") (take first pat)
            asset("s3.private", "doc.pdf") (when multiple paths are specified for the disk)
        """
        ...
    def route(name: str, params: dict = {}, absolute: bool = True) -> str:
        """Generates a fully qualified URL to the given route name.
        Example:
            route("users.home") : http://masonite.app/dashboard/
            route("users.profile", {"id": 1}) : http://masonite.app/users/1/profile/
            route("users.profile", {"id": 1}, absolute=False) : /users/1/profile/
        """
        ...

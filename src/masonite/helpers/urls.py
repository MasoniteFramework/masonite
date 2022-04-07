from os.path import join
from urllib import parse

from ..configuration import config


class UrlsHelper:
    """URLs helper provide handy functions to build URLs."""

    def __init__(self, app):
        self.app = app

    def url(self, path: str = "", query_params: dict = {}) -> str:
        """Generates a fully qualified url to the given path. If no path is given this will return
        the base url domain. A query parameters dictionary can be provided to add query parameters
        to the url."""
        # ensure that no slash is prefixing the relative path
        path_result = parse.urlsplit(path.lstrip("/"))

        # parse existing query parameters
        existing_query_params = dict(parse.parse_qsl(path_result.query))
        all_query_params = {**existing_query_params, **query_params}

        relative_path = path_result.path

        # add query parameters to url if any
        if all_query_params:
            relative_path += "?" + parse.urlencode(all_query_params)

        return join(config("application.app_url"), relative_path)

    def asset(self, alias, filename):
        """Generates a fully qualified URL for the given asset using the given disk
        Example:
            asset("local", "avatar.jpg") (take first pat)
            asset("s3.private", "doc.pdf") (when multiple paths are specified for the disk)
        """
        disks = config("filesystem.disks")
        # ensure that no slash is prefixing the relative filename path
        filename = filename.lstrip("/")
        if "." in alias:
            alias = alias.split(".")
            location = disks[alias[0]]["path"][alias[1]]
        else:
            location = disks[alias]["path"]
            # take first path if no path specified
            if isinstance(location, dict):
                location = list(location.values())[0]
        return join(location, filename)

    def route(
        self, name: str, params: dict = {}, absolute=True, query_params: dict = {}
    ) -> str:
        """Generates a fully qualified URL to the given route name.
        Example:
            route("users.home") : http://masonite.app/dashboard/
            route("users.profile", {"id": 1}) : http://masonite.app/users/1/profile/
            route("users.profile", {"id": 1}, query_params={"section": "infos"}) :
                http://masonite.app/users/1/profile/?section=info
            route("users.profile", {"id": 1}, absolute=False) : /users/1/profile/
        """

        relative_url = self.app.make("router").route(name, params, query_params)
        if absolute:
            return self.url(relative_url)
        else:
            return relative_url

"""Helper Functions for RouteProvider."""

import re
from urllib.parse import parse_qs

from .misc import deprecated


def flatten_routes(routes):
    """Flatten the grouped routes into a single list of routes.

    Arguments:
        routes {list} -- This can be a multi dementional list which can flatten all lists into a single list.

    Returns:
        list -- Returns the flatten list.
    """
    route_collection = []
    for route in routes:
        if isinstance(route, list):
            for r in flatten_routes(route):
                route_collection.append(r)
        else:
            route_collection.append(route)

    return route_collection


def compile_route_to_regex(route):
    """Compile a route to regex.

    Arguments:
        route {masonite.routes.Route} -- The Masonite route object

    Returns:
        string -- Returns the regex of the route.
    """
    # Split the route
    split_given_route = route.split("/")

    # compile the provided url into regex
    url_list = []
    regex = "^"
    for regex_route in split_given_route:
        if "*" in regex_route or "@" in regex_route:
            if ":int" in regex_route:
                regex += r"(\d+)"
            elif ":string" in regex_route:
                regex += r"([a-zA-Z]+)"
            else:
                # default
                regex += r"[\w.\-\/]+"
            regex += r"\/"

            # append the variable name passed @(variable):int to a list
            url_list.append(
                regex_route.replace("@", "").replace(":int", "").replace(":string", "")
            )
        else:
            regex += regex_route + r"\/"

    if regex.endswith("/") and not route.endswith("/"):
        regex = regex[:-2]

    regex += "$"

    return regex


def create_matchurl(url, route):
    """Create a regex string for router.url to be matched against.

    Arguments:
        router {masonite.routes.Route} -- The Masonite route object
        route {masonite.routes.BaseHttpRoute} -- The current route being executed.

    Returns:
        string -- compiled regex string
    """

    if route._compiled_regex is None:
        route.compile_route_to_regex()

    if not url.endswith("/"):
        return route._compiled_regex
    elif url == "/":
        return route._compiled_regex

    return route._compiled_regex_end


def query_parse(query_string):
    d = {}
    for key, value in parse_qs(query_string).items():
        regex_match = re.match(r"(?P<key>[^\[]+)\[(?P<value>[^\]]+)\]", key)
        if regex_match:
            gd = regex_match.groupdict()
            d.setdefault(gd["key"], {})[gd["value"]] = value[0]
        else:
            d.update({key: value[0]})

    return d

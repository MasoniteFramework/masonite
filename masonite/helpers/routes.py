"""Helper Functions for RouteProvider."""

import re
from masonite.helpers import deprecated


def flatten_routes(routes):
    """Flatten the grouped routes into a single list of routes.

    Arguments:
        routes {list} -- This can be a multi dementional list which can flatten all lists into a single list.

    Returns:
        list -- Returns the flatten list.
    """
    route_collection = []
    for route in routes:
        # Check if a route is a list of routes
        if isinstance(route, list):
            for r in flatten_routes(route):
                route_collection.append(r)
        else:
            route_collection.append(route)

    return route_collection


DEPRECATION_STRING = " Please use the class based version of the route. Please visit {} for more information".format('https://docs.masoniteproject.com/prologue/deprecation#helper-functions')


@deprecated("The 'get' route helper is deprecated. {}".format(DEPRECATION_STRING))
def get(url, controller):
    """Shortcut for Get HTTP class.

    Arguments:
        url {string} -- The url you want to use for the route
        controller {string|object} -- This can be a string controller or a normal object controller

    Returns:
        masonite.routes.Get -- The Masonite Get class.
    """
    from masonite.routes import Get

    return Get().route(url, controller)


@deprecated("The 'match' route helper is deprecated. {}".format(DEPRECATION_STRING))
def match(method_type, url, controller):
    """Shortcut for Match HTTP class.

    Arguments:
        method_type {list} -- A list of the method types you want to accept
        url {string} -- The url you want to use for the route
        controller {string|object} -- This can be a string controller or a normal object controller

    Returns:
        masonite.routes.Get -- The Masonite Get class.
    """
    from masonite.routes import Match

    return Match(method_type).route(url, controller)


@deprecated("The 'post' route helper is deprecated. {}".format(DEPRECATION_STRING))
def post(url, controller):
    """Shortcut for Post HTTP class.

    Arguments:
        url {string} -- The url you want to use for the route
        controller {string|object} -- This can be a string controller or a normal object controller

    Returns:
        masonite.routes.Post -- The Masonite Post class.
    """
    from masonite.routes import Post

    return Post().route(url, controller)


@deprecated("The 'delete' route helper is deprecated. {}".format(DEPRECATION_STRING))
def delete(url, controller):
    """Shortcut for Delete HTTP class.

    Arguments:
        url {string} -- The url you want to use for the route
        controller {string|object} -- This can be a string controller or a normal object controller

    Returns:
        masonite.routes.Delete -- The Masonite Delete class.
    """
    from masonite.routes import Delete

    return Delete().route(url, controller)


@deprecated("The 'put' route helper is deprecated. {}".format(DEPRECATION_STRING))
def put(url, controller):
    """Shortcut for Put HTTP class.

    Arguments:
        url {string} -- The url you want to use for the route
        controller {string|object} -- This can be a string controller or a normal object controller

    Returns:
        masonite.routes.Put -- The Masonite Put class.
    """
    from masonite.routes import Put

    return Put().route(url, controller)


@deprecated("The 'patch' route helper is deprecated. {}".format(DEPRECATION_STRING))
def patch(url, controller):
    """Shortcut for Patch HTTP class.

    Arguments:
        url {string} -- The url you want to use for the route
        controller {string|object} -- This can be a string controller or a normal object controller

    Returns:
        masonite.routes.Patch -- The Masonite Patch class.
    """
    from masonite.routes import Patch

    return Patch().route(url, controller)


@deprecated("The 'group' route helper is deprecated. {}".format(DEPRECATION_STRING))
def group(url, route_list):
    """Shortcut for GET HTTP class.

    Arguments:
        url {string} -- The url you want to use for the route
        route_list {list} -- A list of routes

    Returns:
        list -- Returns the list route
    """
    for route in route_list:
        route.route_url = url + route.route_url

    return route_list


def compile_route_to_regex(route):
    """Compile a route to regex.

    Arguments:
        route {masonite.routes.Route} -- The Masonite route object

    Returns:
        string -- Returns the regex of the route.
    """
    # Split the route
    split_given_route = route.split('/')

    # compile the provided url into regex
    url_list = []
    regex = '^'
    for regex_route in split_given_route:
        if '*' in regex_route or '@' in regex_route:
            if ':int' in regex_route:
                regex += r'(\d+)'
            elif ':string' in regex_route:
                regex += r'([a-zA-Z]+)'
            else:
                # default
                regex += r'[([\w.-\]+)]+'
            regex += r'\/'

            # append the variable name passed @(variable):int to a list
            url_list.append(
                regex_route.replace('@', '').replace(
                    ':int', '').replace(':string', '')
            )
        else:
            regex += regex_route + r'\/'

    if regex.endswith('/') and not route.endswith('/'):
        regex = regex[:-2]

    regex += '$'

    return regex


def create_matchurl(router, route):
    """Create a regex string for router.url to be matched against.

    Arguments:
        router {masonite.routes.Route} -- The Masonite route object
        route {masonite.routes.BaseHttpRoute} -- The current route being executed.

    Returns:
        string -- compiled regex string
    """
    # Compiles the given route to regex
    regex = route.compile_route_to_regex(router)

    if route.route_url.endswith('/'):
        if router.url.endswith('/'):
            matchurl = re.compile(regex.replace(r'\/\/$', r'\/$'))
        else:
            matchurl = re.compile(regex.replace(r'\/\/$', r'$'))
    else:
        if router.url.endswith('/'):
            matchurl = re.compile(regex)
        else:
            matchurl = re.compile(regex.replace(r'\/$', r'$'))

    return matchurl

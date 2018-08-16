from masonite.routes import Get, Post, Delete, Patch, Put


def flatten_routes(routes):
    """Flattens the grouped routes into a single list of routes.
    
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


def get(url, controller):
    """Shortcut for Get HTTP class.
    
    Arguments:
        url {string} -- The url you want to use for the route
        controller {string|object} -- This can be a string controller or a normal object controller
    
    Returns:
        masonite.routes.Get -- The Masonite Get class.
    """

    return Get().route(url, controller)


def post(url, controller):
    """Shortcut for Post HTTP class.
    
    Arguments:
        url {string} -- The url you want to use for the route
        controller {string|object} -- This can be a string controller or a normal object controller
    
    Returns:
        masonite.routes.Post -- The Masonite Post class.
    """

    return Post().route(url, controller)


def delete(url, controller):
    """Shortcut for Delete HTTP class.
    
    Arguments:
        url {string} -- The url you want to use for the route
        controller {string|object} -- This can be a string controller or a normal object controller
    
    Returns:
        masonite.routes.Delete -- The Masonite Delete class.
    """

    return Delete().route(url, controller)


def put(url, controller):
    """Shortcut for Put HTTP class.
    
    Arguments:
        url {string} -- The url you want to use for the route
        controller {string|object} -- This can be a string controller or a normal object controller
    
    Returns:
        masonite.routes.Put -- The Masonite Put class.
    """

    return Put().route(url, controller)


def patch(url, controller):
    """Shortcut for Patch HTTP class.
    
    Arguments:
        url {string} -- The url you want to use for the route
        controller {string|object} -- This can be a string controller or a normal object controller
    
    Returns:
        masonite.routes.Patch -- The Masonite Patch class.
    """

    return Patch().route(url, controller)


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
    """Compiles a route to regex
    
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
                regex += r'(\w+)'
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

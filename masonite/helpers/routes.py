from masonite.routes import Get, Post, Delete, Patch, Put


def flatten_routes(routes):
    """
    Flattens the grouped routes into a single list of routes.
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
    """
    Shortcut for GET http
    """
    return Get().route(url, controller)


def post(url, controller):
    """
    Shortcut for POST http
    """
    return Post().route(url, controller)


def delete(url, controller):
    """
    Shortcut for DELETE http
    """
    return Delete().route(url, controller)


def put(url, controller):
    """
    Shortcut for Put http
    """
    return Put().route(url, controller)


def patch(url, controller):
    """
    Shortcut for PATCH http
    """
    return Patch().route(url, controller)


def group(url, route_list):
    """
    Group route
    """
    for route in route_list:
        route.route_url = url + route.route_url

    return route_list

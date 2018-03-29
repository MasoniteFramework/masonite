from masonite.routes import Get, Post, Delete, Patch, Put


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

"""View Helper Module."""

from jinja2 import Markup


def set_request_method(method_type):
    """Return an input string for use in a view to change the request method of a form.

    Arguments:
        method_type {string} -- Can be options like GET, POST, PUT, PATCH, DELETE

    Returns:
        string -- An input string.
    """
    return Markup("<input type='hidden' name='__method' value='{0}'>".format(method_type))


def back(location=None):
    """Return an input element for use in telling Masonite which route to redirect back to.

    Arguments:
        location {string} -- The route to redirect back to.

    Returns:
        string -- An input string.
    """
    if location is None:
        from wsgi import container
        request = container.make('Request')
        intended_route = request.session.get('__intend')
        if intended_route:
            location = intended_route
        else:
            location = request.path

    return Markup("<input type='hidden' name='__back' value='{0}'>".format(location))


def hidden(value, name='hidden-input'):
    return Markup("<input type='hidden' name='{}' value='{}'>".format(name, value))


def old(session_key, default=''):
    """Return the old value submitted by forms validated with Valitators.

    Arguments:
        session_key {string} -- The key flashed to session.

    Returns:
        string -- An input string.
    """

    from wsgi import container
    session_container = container.make('Session')

    if session_container.has(session_key):
        return session_container.get(session_key)
    return default

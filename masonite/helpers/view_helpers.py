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


def back(location):
    """Return an input element for use in telling Masonite which route to redirect back to.

    Arguments:
        location {string} -- The route to redirect back to.

    Returns:
        string -- An input string.
    """
    return Markup("<input type='hidden' name='__back' value='{0}'>".format(location))

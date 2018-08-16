""" View Helper Module """


def set_request_method(method_type):
    """Returns an input string for use in a view to change the request method of a form.

    Arguments:
        method_type {string} -- Can be options like GET, POST, PUT, PATCH, DELETE

    Returns:
        string -- An input string.
    """

    return "<input type='hidden' name='__method' value='{0}'>".format(method_type)


def back(location):
    """Returns an input element for use in telling Masonite which route to redirect back to.

    Arguments:
        location {string} -- The route to redirect back to.

    Returns:
        string -- An input string.
    """

    return "<input type='hidden' name='__back' value='{0}'>".format(location)

def set_request_method(method_type):
    return "<input type='hidden' name='__method' value='{0}'>".format(method_type)


def back(location):
    return "<input type='hidden' name='__back' value='{0}'>".format(location)

"""String generators and helpers"""
import random
import string
from urllib import parse


def random_string(length=4):
    """Generate a random string based on the given length.

    Keyword Arguments:
        length {int} -- The amount of the characters to generate (default: {4})

    Returns:
        string
    """
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )


def modularize(file_path, suffix=".py"):
    """Transforms a file path to a dotted path. On UNIX paths contains / and on Windows \\.

    Keyword Arguments:
        file_path {str} -- A file path such app/controllers

    Returns:
        value {str} -- a dotted path such as app.controllers
    """
    # if the file had the .py extension remove it as it's not needed for a module
    return removesuffix(file_path.replace("/", ".").replace("\\", "."), suffix)


def as_filepath(dotted_path):
    """Inverse of modularize, transforms a dotted path to a file path (with /).

    Keyword Arguments:
        dotted_path {str} -- A dotted path such app.controllers

    Returns:
        value {str} -- a file path such as app/controllers
    """
    return dotted_path.replace(".", "/")


def removeprefix(string, prefix):
    """Implementation of str.removeprefix() function available for Python versions lower than 3.9."""
    if string.startswith(prefix):
        return string[len(prefix) :]
    else:
        return string


def removesuffix(string, suffix):
    """Implementation of str.removesuffix() function available for Python versions lower than 3.9."""
    if suffix and string.endswith(suffix):
        return string[: -len(suffix)]
    else:
        return string


def add_query_params(url: str, query_params: dict) -> str:
    """Add query params dict to a given url (which can already contain some query parameters)."""
    path_result = parse.urlsplit(url)

    base_url = path_result.path

    # parse existing query parameters if any
    existing_query_params = dict(parse.parse_qsl(path_result.query))
    all_query_params = {**existing_query_params, **query_params}

    # add query parameters to url if any
    if all_query_params:
        base_url += "?" + parse.urlencode(all_query_params)

    return base_url

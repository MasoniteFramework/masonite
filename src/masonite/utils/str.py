"""String generators and helpers"""
import random
import string


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


def match(string: str, ref_string: str) -> str:
    """Check if a given string matches a reference string. Wildcard '*' can be used at start, end
    or middle of the string."""
    if ref_string.startswith("*"):
        ref_string = ref_string.replace("*", "")
        return string.endswith(ref_string)
    elif ref_string.endswith("*"):
        ref_string = ref_string.replace("*", "")
        return string.startswith(ref_string)
    elif "*" in ref_string:
        split_search = ref_string.split("*")
        return string.startswith(split_search[0]) and string.endswith(split_search[1])
    else:
        return ref_string == string

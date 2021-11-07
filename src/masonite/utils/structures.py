"""Helpers for multiple data structures"""
import importlib
from importlib.abc import Loader
from dotty_dict import dotty

from ..exceptions.exceptions import LoaderNotFound

from .str import modularize


def load(path, object_name=None, default=None, raise_exception=False):
    """Load the given object from a Python module located at path and returns a default
    value if not found. If no object name is provided, loads the module.

    Arguments:
        path {str} -- A file path or a dotted path of a Python module
        object {str} -- The object name to load in this module (None)
        default {str} -- The default value to return if object not found in module (None)
    Returns:
        {object} -- The value (or default) read in the module or the module if no object name
    """
    # modularize path if needed
    module_path = modularize(path)
    # module = pydoc.locate(dotted_path)
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError:
        if raise_exception:
            raise LoaderNotFound(
                f"{module_path} not found or error when importing this module."
            )
        return None

    if object_name is None:
        return module
    else:
        try:
            return getattr(module, object_name)
        except KeyError:
            if raise_exception:
                raise LoaderNotFound(f"{object_name} not found in {module_path}")
            else:
                return default


def data(dictionary={}):
    """Transform the given dictionary to be read/written with dot notation.

    Arguments:
        dictionary {dict} -- a dictionary structure

    Returns:
        {dict} -- A dot dictionary
    """
    return dotty(dictionary)


def data_get(dictionary, key, default=None):
    """Read dictionary value from key using nested notation.

    Arguments:
        dictionary {dict} -- a dictionary structure
        key {str} -- the dotted (or not) key to look for
        default {object} -- the default value to return if the key does not exist (None)

    Returns:
        value {object}
    """
    # dotty dict uses : instead of * for wildcards
    dotty_key = key.replace("*", ":")
    return data(dictionary).get(dotty_key, default)


def data_set(dictionary, key, value, overwrite=True):
    """Set dictionary value at key using nested notation. Values are overriden by default but
    this behaviour can be changed by passing overwrite=False.
    The dictionary is edited in place but is also returned.

    Arguments:
        dictionary {dict} -- a dictionary structure
        key {str} -- the dotted (or not) key to set
        value {object} -- the value to set at key
        overwrite {bool} -- override the value if key exists in dictionary (True)

    Returns:
        dictionary {dict} -- the edited dictionary
    """
    if "*" in key:
        raise ValueError("You cannot set values with wildcards *")
    if not overwrite and data_get(dictionary, key):
        return
    data(dictionary)[key] = value
    return dictionary

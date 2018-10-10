"""Static Helper Module."""

from config.storage import DRIVERS


def static(alias, file_name):
    """Get the static file location of an asset.

    Arguments:
        alias {string} -- The driver and location to search for. This could be s3.uploads
        file_name {string} -- The filename of the file to return.

    Returns:
        string -- Returns the file location.
    """
    if '.' in alias:
        alias = alias.split('.')
        location = DRIVERS[alias[0]]['location'][alias[1]]
        if location.endswith('/'):
            location = location[:-1]

        return '{}/{}'.format(location, file_name)

    location = DRIVERS[alias]['location']
    if isinstance(location, dict):
        location = list(location.values())[0]
        if location.endswith('/'):
            location = location[:-1]

    return '{}/{}'.format(location, file_name)

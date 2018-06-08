from config.storage import DRIVERS

def static(alias, file_name):
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

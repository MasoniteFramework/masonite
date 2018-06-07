from config.storage import DRIVERS

def static(alias, file_name):
    if '.' in alias:
        alias = alias.split('.')
        return '{}/{}'.format(DRIVERS[alias[0]]['location'][alias[1]], file_name)

    return '{}/{}'.format(DRIVERS[alias]['location'], file_name)

from ..facades import Config


def config(key, default=None):
    return Config.get(key, default)

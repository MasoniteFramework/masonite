

class ConfigRepository(object):

    def __init__(self):
        self._items = {"config": {}}

    def has(self, key):
        # TODO: implement for nested
        return key in self._items["config"].keys()

    def get(self, key, default=None):
        return self._items.get(key, default)

    def _set(self, key, value=None):
        self._items["config"].update({key: value})

    def all(self):
        return self._items

    def __getitem__(self, attr_name):
        return self._items["config"][attr_name]

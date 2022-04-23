import os

from ..utils.filesystem import get_extension


class FileStream:
    def __init__(self, stream, name=None):
        self.stream = stream
        self._name = name

    def path(self):
        return self.stream.name

    def extension(self):
        return get_extension(self._name or self.path())

    def name(self):
        return self._name or os.path.basename(self.path())

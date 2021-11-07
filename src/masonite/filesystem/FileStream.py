import os


class FileStream:
    def __init__(self, stream, name=None):
        self.stream = stream
        self._name = name

    def path(self):
        return self.stream.name

    def extension(self):
        return os.path.splitext(self._name or self.path())[1]

    def name(self):
        return self._name or os.path.basename(self.path())

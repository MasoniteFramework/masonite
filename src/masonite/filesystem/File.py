import hashlib

from ..utils.filesystem import get_extension


class File:
    def __init__(self, content, filename=None):
        self.content = content
        self.filename = filename

    def path(self):
        pass

    def extension(self):
        return get_extension(self.filename)

    def name(self):
        return self.filename

    def stream(self):
        return self.content

    def hash_path_name(self):
        return f"{self.hash_name()}{self.extension()}"

    def hash_name(self):
        return hashlib.sha1(bytes(self.name(), "utf-8")).hexdigest()

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name()})"

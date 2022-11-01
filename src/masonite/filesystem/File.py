import hashlib

from ..utils.filesystem import get_extension


class File:
    """Base Masonite File class."""

    def __init__(self, content: bytes, filename: str = None):
        self.content = content
        self.filename = filename

    def path(self):
        pass

    def extension(self) -> str:
        """Get file extension (with the dot)."""
        return get_extension(self.filename)

    def name(self) -> str:
        """Get the name of the file with the extension."""
        return self.filename

    def stream(self) -> bytes:
        """Get file content."""
        return self.content

    def hash_path_name(self) -> str:
        """Get a hashed version of the file name (with extension)."""
        return f"{self.hash_name()}{self.extension()}"

    def hash_name(self) -> str:
        """Get a hashed version of the file name (without extension)."""
        return hashlib.sha1(bytes(self.name(), "utf-8")).hexdigest()

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name()})"

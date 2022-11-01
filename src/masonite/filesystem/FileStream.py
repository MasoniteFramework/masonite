import os

from ..utils.filesystem import get_extension


class FileStream:
    """Base Masonite FileStream class."""

    def __init__(self, stream: bytes, name: str = None):
        self.stream = stream
        self._name = name

    def path(self) -> str:
        """Get the path of the file."""
        return self.stream.name

    def extension(self) -> str:
        """Get file extension (with the dot)."""
        return get_extension(self._name or self.path())

    def name(self) -> str:
        """Get the name of the file with the extension."""
        return self._name or os.path.basename(self.path())

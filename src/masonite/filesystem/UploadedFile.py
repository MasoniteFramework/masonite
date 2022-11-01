import hashlib

from ..utils.filesystem import get_extension


class UploadedFile:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.content = content

    def extension(self) -> str:
        """Get file extension (with the dot)."""
        return get_extension(self.filename)

    @property
    def name(self) -> str:
        """Get the name of the file with the extension."""
        return self.filename

    def path_name(self) -> str:
        """Get file path."""
        return f"{self.name}{self.extension()}"

    def hash_path_name(self) -> str:
        """Get a hashed version of the file name (with extension)."""
        return f"{self.hash_name()}{self.extension()}"

    def stream(self) -> bytes:
        """Get file content."""
        return self.content

    def hash_name(self) -> str:
        """Get a hashed version of the file name (without extension)."""
        return hashlib.sha1(bytes(self.name(), "utf-8")).hexdigest()

    def get_content(self) -> bytes:
        """Get file content."""
        return self.content

    @property
    def size(self) -> int:
        """Get file size in bytes."""
        return len(self.content)

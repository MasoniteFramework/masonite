import os
import uuid
from os.path import isfile, join
from shutil import copyfile, move
from typing import TYPE_CHECKING, List

from ..FileStream import FileStream
from ..File import File
from ...utils.filesystem import get_extension

if TYPE_CHECKING:
    from ...foundation import Application
    from ..UploadedFile import UploadedFile


class LocalDriver:
    """File manager driver using local filesystem on the server."""

    def __init__(self, application: "Application"):
        self.application = application
        self.options: dict = {}

    def set_options(self, options: dict) -> "LocalDriver":
        self.options = options
        return self

    def get_path(self, path: str):
        """Get absolute file path to given relative path."""
        file_path = os.path.join(self.options.get("path"), path)
        self.make_file_path_if_not_exists(file_path)
        return file_path

    def get_name(self, path: str, alias: str):
        """Build a filename with given alias based on path extension."""
        extension = get_extension(path)
        return f"{alias}{extension}"

    def put(self, file_path: str, content: str) -> str:
        """Save content string in file at given path."""
        with open(self.get_path(os.path.join(file_path)), "w") as f:
            f.write(content)
        return content

    def put_file(
        self, file_path: str, content: "bytes|UploadedFile", name: str = None
    ) -> str:
        """Save content at the given path. Name of the file can be provided else it will
        be an auto generated uuid name."""
        file_name = self.get_name(content.name, name or str(uuid.uuid4()))

        if hasattr(content, "get_content"):
            content = content.get_content()

        if isinstance(content, str):
            content = bytes(content, "utf-8")

        with open(self.get_path(os.path.join(file_path, file_name)), "wb") as f:
            f.write(content)

        return os.path.join(file_path, file_name)

    def get(self, file_path: str) -> str:
        """Get file content at the given path."""
        try:
            with open(self.get_path(file_path), "r") as f:
                content = f.read()

            return content
        except FileNotFoundError:
            return None

    def exists(self, file_path: str) -> bool:
        """Check if the given file path exists on the local configured disk."""
        return os.path.exists(self.get_path(file_path))

    def missing(self, file_path: str) -> bool:
        """Check if the given file path is missing on the local configured disk."""
        return not self.exists(file_path)

    def stream(self, file_path: str) -> "FileStream":
        """Returns a FileStream instance of the file located at the given path."""
        with open(self.get_path(file_path), "r") as f:
            content = f
        return FileStream(content)

    def copy(self, from_file_path: str, to_file_path: str) -> str:
        """Copy given source path to destination path."""
        return copyfile(from_file_path, to_file_path)

    def move(self, from_file_path: str, to_file_path: str) -> str:
        """Move given source path to destination path."""
        return move(self.get_path(from_file_path), self.get_path(to_file_path))

    def prepend(self, file_path: str, content: str) -> str:
        """Add given content string at the beginning of file located at given path."""
        value = self.get(file_path)
        content = content + value
        self.put(file_path, content)
        return content

    def append(self, file_path: str, content: str) -> str:
        """Add given content string at the end of file located at given path."""
        with open(self.get_path(file_path), "a") as f:
            f.write(content)
        return content

    def delete(self, file_path: str) -> None:
        """Remove file located at the given path on the local configured disk."""
        return os.remove(self.get_path(file_path))

    def make_directory(self, directory):
        pass

    def store(self, file: "File|UploadedFile", name: str = None) -> str:
        """Store the given file instance on the local configured disk. If name is provided it
        will be stored under that name else the name will be inferred from the given file name
        hash."""
        if name:
            name = f"{name}{file.extension()}"
        full_path = self.get_path(name or file.hash_path_name())
        with open(full_path, "wb") as f:
            f.write(file.stream())

        return full_path

    def make_file_path_if_not_exists(self, file_path: str) -> bool:
        """Create full path to given file path is it does not exist."""
        if not os.path.isfile(file_path):
            if not os.path.exists(os.path.dirname(file_path)):
                # Create the path to the model if it does not exist
                os.makedirs(os.path.dirname(file_path))

            return True

        return False

    def get_files(self, directory: str = "") -> List[File]:
        """Get a list of File instances located in the given directory on the local file system."""
        file_path = self.get_path(directory)
        files = []
        for f in os.listdir(file_path):
            if not isfile(join(file_path, f)):
                continue

            files.append(File(self.get(f), f))

        return files

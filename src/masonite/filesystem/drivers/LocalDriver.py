import os
from shutil import copyfile, move
from ..FileStream import FileStream
from ..File import File
import uuid
import os
from os.path import isfile, join


class LocalDriver:
    def __init__(self, application):
        self.application = application
        self.options = {}

    def set_options(self, options):
        self.options = options
        return self

    def get_path(self, path):
        file_path = os.path.join(self.options.get("path"), path)
        self.make_file_path_if_not_exists(file_path)
        return file_path

    def get_name(self, path, alias):
        extension = os.path.splitext(path)[1]
        return f"{alias}{extension}"

    def put(self, file_path, content):
        with open(self.get_path(os.path.join(file_path)), "w") as f:
            f.write(content)
        return content

    def put_file(self, file_path, content, name=None):
        file_name = self.get_name(content.name, name or str(uuid.uuid4()))

        if hasattr(content, "get_content"):
            content = content.get_content()

        if isinstance(content, str):
            content = bytes(content, "utf-8")

        with open(self.get_path(os.path.join(file_path, file_name)), "wb") as f:
            f.write(content)

        return os.path.join(file_path, file_name)

    def get(self, file_path):
        try:
            with open(self.get_path(file_path), "r") as f:
                content = f.read()

            return content
        except FileNotFoundError:
            return None

    def exists(self, file_path):
        return os.path.exists(self.get_path(file_path))

    def missing(self, file_path):
        return not self.exists(file_path)

    def stream(self, file_path):
        with open(self.get_path(file_path), "r") as f:
            content = f
        return FileStream(content)

    def copy(self, from_file_path, to_file_path):
        return copyfile(from_file_path, to_file_path)

    def move(self, from_file_path, to_file_path):
        return move(self.get_path(from_file_path), self.get_path(to_file_path))

    def prepend(self, file_path, content):
        value = self.get(file_path)
        content = content + value
        self.put(file_path, content)
        return content

    def append(self, file_path, content):
        with open(self.get_path(file_path), "a") as f:
            f.write(content)
        return content

    def delete(self, file_path):
        return os.remove(self.get_path(file_path))

    def make_directory(self, directory):
        pass

    def store(self, file, name=None):
        if name:
            name = f"{name}{file.extension()}"
        full_path = self.get_path(name or file.hash_path_name())
        with open(full_path, "wb") as f:
            f.write(file.stream())

        return full_path

    def make_file_path_if_not_exists(self, file_path):
        if not os.path.isfile(file_path):
            if not os.path.exists(os.path.dirname(file_path)):
                # Create the path to the model if it does not exist
                os.makedirs(os.path.dirname(file_path))

            return True

        return False

    def get_files(self, directory=""):
        file_path = self.get_path(directory)
        files = []
        for f in os.listdir(file_path):
            if not isfile(join(file_path, f)):
                continue

            files.append(File(self.get(f), f))

        return files

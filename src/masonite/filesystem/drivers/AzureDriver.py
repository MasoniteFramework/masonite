import os
import uuid

from ..FileStream import FileStream
from ..File import File


class AzureDriver:
    def __init__(self, application):
        self.application = application
        self.options = {}
        self.connection = None

    def set_options(self, options):
        self.options = options
        return self

    def get_connection(self):
        try:
            from azure.storage.file import FileService
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'azure-storage-file' library. Run 'pip install azure-storage-file' to fix this."
            )

        if not self.connection:
            self.connection = FileService(
                account_name=self.options.get("account_name"),
                account_key=self.options.get("access_key"),
            )

        return self.connection

    def get_share(self):
        return self.options.get("share")

    def get_name(self, path, alias):
        extension = os.path.splitext(path)[1]
        return f"{alias}{extension}"

    def put(self, file_path, content):
        directory, filename = os.path.split(file_path)
        self.get_connection().create_file_from_bytes(
            self.get_share(), directory, filename, content
        )
        return content

    def put_file(self, file_path, content, name=None):
        file_name = self.get_name(content.name, name or str(uuid.uuid4()))

        if hasattr(content, "get_content"):
            content = content.get_content()

        self.get_connection().create_file_from_bytes(
            self.get_share(), file_path, file_name, content
        )
        return os.path.join(file_path, file_name)

    def get(self, file_path):
        directory, filename = os.path.split(file_path)
        try:
            return self.get_connection().get_file_to_bytes(
                self.get_share(), directory, filename
            )
        except self.missing_file_exceptions():
            pass

    def missing_file_exceptions(self):
        import azure

        return (azure.core.exceptions.ResourceNotFoundError,)

    def exists(self, file_path):
        directory, filename = os.path.split(file_path)
        try:
            self.get_connection().get_file_to_bytes(
                self.get_share(), directory, filename
            )
            return True
        except self.missing_file_exceptions():
            return False

    def missing(self, file_path):
        return not self.exists(file_path)

    def stream(self, file_path):
        directory, filename = os.path.split(file_path)
        return FileStream(
            self.get_connection().get_file_to_bytes(
                self.get_share(), directory, filename
            ),
            file_path,
        )

    def copy(self, from_file_path, to_file_path):
        return NotImplementedError("AzureDriver.copy() is not implemented yet.")

    def move(self, from_file_path, to_file_path):
        self.copy(from_file_path, to_file_path)
        self.delete(from_file_path)

    def prepend(self, file_path, content):
        value = self.get(file_path)
        content = content + value
        self.put(file_path, content)
        return content

    def append(self, file_path, content):
        value = self.get(file_path) or ""
        value += content
        self.put(file_path, content)

    def delete(self, file_path):
        directory, filename = os.path.split(file_path)
        return self.get_connection().delete_file(self.get_share(), directory, filename)

    def store(self, file, name=None):
        full_path = name or file.hash_path_name()
        directory, filename = os.path.split(full_path)
        self.get_connection().create_file_from_stream(
            self.get_share(), directory, filename, file.stream()
        )
        return full_path

    def make_file_path_if_not_exists(self, file_path):
        if not os.path.isfile(file_path):
            if not os.path.exists(os.path.dirname(file_path)):
                # Create the path to the model if it does not exist
                os.makedirs(os.path.dirname(file_path))

            return True

        return False

    def get_files(self, directory=None):
        files_generator = self.get_connection().list_directories_and_files(
            self.get_share(), directory_name=directory
        )
        files = []
        for obj in files_generator:
            files.append(File(obj, obj.name))

        return files

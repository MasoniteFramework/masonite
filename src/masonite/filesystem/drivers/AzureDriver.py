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
            from azure.storage.blob import BlobServiceClient
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'azure-storage-blob' library. Run 'pip install azure-storage-blob' to fix this."
            )

        if not self.connection:
            self.connection = BlobServiceClient(
                account_url=self.options.get("account_url"),
                credential=self.options.get("access_key"),
            )

        return self.connection

    def get_container(self):
        return self.options.get("container")

    def get_share(self):
        return self.options.get("share")

    def get_name(self, path, alias):
        extension = os.path.splitext(path)[1]
        return f"{alias}{extension}"

    def put(self, file_path, content):
        # Create blob with same name as local file name
        blob_client = self.get_connection().get_blob_client(
            container=self.get_container(), blob=file_path
        )

        # Create blob on storage
        # Overwrite if it already exists!
        blob_client.upload_blob(
            content,
            overwrite=True,
        )

        return content

    def put_file(self, file_path, content, name=None):
        file_name = self.get_name(content.name, name or str(uuid.uuid4()))

        if hasattr(content, "get_content"):
            content = content.get_content()

        # Create blob with same name as local file name
        blob_client = self.get_connection().get_blob_client(
            container=self.get_container(), blob=file_path
        )

        # Create blob on storage
        # Overwrite if it already exists!
        blob_client.upload_blob(content, overwrite=True)

        return os.path.join(file_path, file_name)

    def get(self, file_path):
        blob_client = self.get_connection().get_blob_client(
            container=self.get_container(), blob=file_path
        )
        try:
            return blob_client.download_blob().readall().decode("utf-8")
        except self.missing_file_exceptions():
            pass

    def missing_file_exceptions(self):
        import azure

        return (azure.core.exceptions.ResourceNotFoundError,)

    def exists(self, file_path):
        return (
            self.get_connection()
            .get_blob_client(container=self.get_container(), blob=file_path)
            .exists()
        )

    def missing(self, file_path):
        return not self.exists(file_path)

    def stream(self, file_path):
        blob_client = self.get_connection().get_blob_client(
            container=self.get_container(), blob=file_path
        )
        return FileStream(
            blob_client.download_blob().readall(),
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
        blob_client = self.get_connection().get_blob_client(
            container=self.get_container(), blob=file_path
        )
        return blob_client.delete_blob()

    def store(self, file, name=None):
        full_path = name or file.hash_path_name()

        blob_client = self.get_connection().get_blob_client(
            container=self.get_container(), blob=full_path
        )
        blob_client.upload_blob(file.stream(), overwrite=True)

        return full_path

    def make_file_path_if_not_exists(self, file_path):
        if not os.path.isfile(file_path):
            if not os.path.exists(os.path.dirname(file_path)):
                # Create the path to the model if it does not exist
                os.makedirs(os.path.dirname(file_path))

            return True

        return False

    def get_files(self, directory=None):
        container_client = self.get_connection().get_container_client(
            container=self.get_container()
        )
        if directory:
            objects = container_client.walk_blobs(name_starts_with=directory)
        else:
            objects = container_client.walk_blobs()
        files = []
        for obj in objects:
            files.append(File(obj, obj.name))

        return files

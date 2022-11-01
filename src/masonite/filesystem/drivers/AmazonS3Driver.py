import os
import uuid
from typing import TYPE_CHECKING, List

from ..FileStream import FileStream
from ..File import File
from ...utils.filesystem import get_extension

if TYPE_CHECKING:
    from ...foundation import Application
    from ..UploadedFile import UploadedFile
    from boto3 import Session


class AmazonS3Driver:
    """File manager driver using AWS S3 cloud file storage."""

    def __init__(self, application: "Application"):
        self.application = application
        self.options: dict = {}
        self.connection: Session = None

    def set_options(self, options: dict) -> "AmazonS3Driver":
        self.options = options
        return self

    def get_connection(self) -> "Session":
        """Get the connection to the configured Amazon S3 instance."""
        try:
            import boto3
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'boto3' library. Run 'pip install boto3' to fix this."
            )

        if not self.connection:
            self.connection = boto3.Session(
                aws_access_key_id=self.options.get("client"),
                aws_secret_access_key=self.options.get("secret"),
                region_name=self.options.get("region"),
            )

        return self.connection

    def get_bucket(self) -> str:
        """Get S3 bucket name"""
        return self.options.get("bucket")

    def get_name(self, path: str, alias: str):
        """Build a filename with given alias based on path extension."""
        extension = get_extension(path)
        return f"{alias}{extension}"

    def put(self, file_path: str, content: str) -> str:
        """Save content string in file at given path."""
        self.get_connection().resource("s3").Bucket(self.get_bucket()).put_object(
            Key=file_path, Body=content
        )
        return content

    def put_file(
        self, file_path: str, content: "bytes|UploadedFile", name: str = None
    ) -> str:
        """Save content at the given path. Name of the file can be provided else it will
        be an auto generated uuid name."""
        file_name = self.get_name(content.name, name or str(uuid.uuid4()))

        if hasattr(content, "get_content"):
            content = content.get_content()

        self.get_connection().resource("s3").Bucket(self.get_bucket()).put_object(
            Key=os.path.join(file_path, file_name), Body=content
        )
        return os.path.join(file_path, file_name)

    def get(self, file_path: str) -> str:
        """Get file content at the given path."""
        try:
            return (
                self.get_connection()
                .resource("s3")
                .Bucket(self.get_bucket())
                .Object(file_path)
                .get()
                .get("Body")
                .read()
                .decode("utf-8")
            )
        except self.missing_file_exceptions():
            pass

    def missing_file_exceptions(self):
        import boto3

        return (boto3.exceptions.botocore.errorfactory.ClientError,)

    def exists(self, file_path: str) -> bool:
        """Check if the given file path exists on the local configured disk."""
        try:
            self.get_connection().resource("s3").Bucket(self.get_bucket()).Object(
                file_path
            ).get().get("Body").read()
            return True
        except self.missing_file_exceptions():
            return False

    def missing(self, file_path: str) -> bool:
        """Check if the given file path is missing on the local configured disk."""
        return not self.exists(file_path)

    def stream(self, file_path: str) -> "FileStream":
        """Returns a FileStream instance of the file located at the given path."""
        return FileStream(
            self.get_connection()
            .resource("s3")
            .Bucket(self.get_bucket())
            .Object(file_path)
            .get()
            .get("Body")
            .read(),
            file_path,
        )

    def copy(self, from_file_path: str, to_file_path: str) -> str:
        """Copy given source path to destination path."""
        copy_source = {"Bucket": self.get_bucket(), "Key": from_file_path}
        self.get_connection().resource("s3").meta.client.copy(
            copy_source, self.get_bucket(), to_file_path
        )

    def move(self, from_file_path: str, to_file_path: str) -> str:
        """Move given source path to destination path."""
        self.copy(from_file_path, to_file_path)
        self.delete(from_file_path)

    def prepend(self, file_path: str, content: str) -> str:
        """Add given content string at the beginning of file located at given path."""
        value = self.get(file_path)
        content = content + value
        self.put(file_path, content)
        return content

    def append(self, file_path: str, content: str) -> str:
        """Add given content string at the end of file located at given path."""
        value = self.get(file_path) or ""
        value += content
        self.put(file_path, content)

    def delete(self, file_path: str) -> None:
        """Remove file located at the given path on the local configured disk."""
        return (
            self.get_connection()
            .resource("s3")
            .Object(self.get_bucket(), file_path)
            .delete()
        )

    def store(self, file: "File|UploadedFile", name: str = None) -> str:
        """Store the given file instance on the local configured disk. If name is provided it
        will be stored under that name else the name will be inferred from the given file name
        hash."""
        full_path = name or file.hash_path_name()
        self.get_connection().resource("s3").Bucket(self.get_bucket()).put_object(
            Key=full_path, Body=file.stream()
        )
        return full_path

    def get_files(self, directory: str = "") -> List[File]:
        """Get a list of File instances located in the given directory on the local file system."""
        bucket = self.get_connection().resource("s3").Bucket(self.get_bucket())

        if directory:
            objects = bucket.objects.all().filter(Prefix=directory)
        else:
            objects = bucket.objects.all()

        files = []
        for my_bucket_object in objects.all():
            if "/" not in my_bucket_object.key:
                files.append(File(my_bucket_object, my_bucket_object.key))

        return files

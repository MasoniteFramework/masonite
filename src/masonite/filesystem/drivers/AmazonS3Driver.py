import os
from shutil import copyfile, move
from ..FileStream import FileStream
from ..File import File
import uuid


class AmazonS3Driver:
    def __init__(self, application):
        self.application = application
        self.options = {}
        self.connection = None

    def set_options(self, options):
        self.options = options
        return self

    def get_connection(self):
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

    def get_bucket(self):
        return self.options.get("bucket")

    def get_name(self, path, alias):
        extension = os.path.splitext(path)[1]
        return f"{alias}{extension}"

    def put(self, file_path, content):
        self.get_connection().resource("s3").Bucket(self.get_bucket()).put_object(
            Key=file_path, Body=content
        )
        return content

    def put_file(self, file_path, content, name=None):
        file_name = self.get_name(content.name, name or str(uuid.uuid4()))

        if hasattr(content, "get_content"):
            content = content.get_content()

        self.get_connection().resource("s3").Bucket(self.get_bucket()).put_object(
            Key=os.path.join(file_path, file_name), Body=content
        )
        return os.path.join(file_path, file_name)

    def get(self, file_path):
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

    def exists(self, file_path):
        try:
            self.get_connection().resource("s3").Bucket(self.get_bucket()).Object(
                file_path
            ).get().get("Body").read()
            return True
        except self.missing_file_exceptions():
            return False

    def missing(self, file_path):
        return not self.exists(file_path)

    def stream(self, file_path):
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

    def copy(self, from_file_path, to_file_path):
        copy_source = {"Bucket": self.get_bucket(), "Key": from_file_path}
        self.get_connection().resource("s3").meta.client.copy(
            copy_source, self.get_bucket(), to_file_path
        )

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
        return (
            self.get_connection()
            .resource("s3")
            .Object(self.get_bucket(), file_path)
            .delete()
        )

    def store(self, file, name=None):
        full_path = name or file.hash_path_name()
        self.get_connection().resource("s3").Bucket(self.get_bucket()).put_object(
            Key=full_path, Body=file.stream()
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

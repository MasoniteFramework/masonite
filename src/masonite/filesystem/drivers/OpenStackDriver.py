import os
import uuid

from ..FileStream import FileStream
from ..File import File


class OpenStackDriver:
    """Driver for OpenStack Object Storage.
    API Doc: https://docs.openstack.org/openstacksdk/latest//user/proxies/object_store.html
    """

    def __init__(self, application):
        self.application = application
        self.options = {}
        self.connection = None

    def set_options(self, options):
        self.options = options
        return self

    def get_connection(self):
        try:
            import openstack
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find 'openstacksdk' library. Run 'pip install openstacksdk' to fix this."
            )

        if not self.connection:
            self.connection = openstack.connect(
                auth_url=self.options.get("auth_url"),
                project_name=self.options.get("project_name"),
                username=self.options.get("username"),
                password=self.options.get("password"),
                region_name=self.options.get("region"),
                user_domain_name=self.options.get("user_domain"),
                project_domain_name=self.options.get("project_domain"),
                app_name=self.options.get("app_name"),
                app_version=self.options.get("app_version"),
            )

        return self.connection

    def get_container(self):
        return self.options.get("container")

    def get_name(self, path, alias):
        extension = os.path.splitext(path)[1]
        return f"{alias}{extension}"

    def put(self, file_path, content):
        self.get_connection().object_store.create_object(
            self.get_container(), file_path, data=content
        )
        return content

    def put_file(self, file_path, content, name=None):
        file_name = self.get_name(content.name, name or str(uuid.uuid4()))
        abs_file_path = os.path.join(file_path, file_name)

        if hasattr(content, "get_content"):
            content = content.get_content()

        self.get_connection().object_store.create_object(
            self.get_container(), abs_file_path, data=content
        )

        return abs_file_path

    def get(self, file_path):
        try:
            return self.get_connection().object_store.get_object(
                self.get_container(), file_path
            )
        except self.missing_file_exceptions():
            pass

    def missing_file_exceptions(self):
        import openstack

        return (openstack.exceptions.ResourceNotFound,)

    def exists(self, file_path):
        try:
            self.get_connection().object_store.get_object(
                self.get_container(), file_path
            )
            return True
        except self.missing_file_exceptions():
            return False

    def missing(self, file_path):
        return not self.exists(file_path)

    def stream(self, file_path):
        return FileStream(
            self.get_connection().object_store.stream_object(
                self.get_container(), file_path
            ),
            file_path,
        )

    def copy(self, from_file_path, to_file_path):
        # TODO: try to understand how to implement this
        raise NotImplementedError("OpenStackDriver.copy() is not implemented for now.")

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
        return self.get_connection().object_store.delete_object(
            self.get_container(), file_path
        )

    def store(self, file, name=None):
        full_path = name or file.hash_path_name()
        self.get_connection().object_store.create_object(
            self.get_container(), full_path, data=file.stream()
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
        files = []
        for obj in self.get_connection().object_store.list_objects(
            self.get_container()
        ):
            if directory:
                head, _ = os.path.split(obj.name)
                if head:
                    dirs = head.split("/")
                    if dirs[0] == directory:
                        files.append(File(obj.data, obj.name))
            else:
                files.append(File(obj.data, obj.name))

        return files

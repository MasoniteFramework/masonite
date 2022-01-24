"""New Controller Command."""
import inflection
import os
from ..utils.location import controllers_path
from ..utils.filesystem import get_module_dir, render_stub_file
from .Command import Command


class MakeControllerCommand(Command):
    """
    Creates a new controller class.

    controller
        {name : Name of the controller}
        {--r|--resource : Create a "resource" controller with the usual CRUD methods}
        {--a|--api : Create an "api" controller with the usual CRUD methods}
        {--f|force=? : Force overriding file if already exists}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):

        full_path = self.argument("name")

        if "/" in full_path:
            name = inflection.camelize(os.path.basename(full_path))
            parent_directory = os.path.dirname(full_path)
        else:
            name = inflection.camelize(full_path)
            parent_directory = ""

        folder_controller = controllers_path(parent_directory)
        os.makedirs(folder_controller, exist_ok=True)

        if not name.endswith("Controller"):
            name += "Controller"

        # create a resource controller if required
        if self.option("resource"):
            stub_path = self.get_resource_controller_path()
        elif self.option("api"):
            stub_path = self.get_api_controller_path()
        else:
            stub_path = self.get_basic_controller_path()

        content = render_stub_file(stub_path, name)

        filename = f"{name}.py"
        full_path_with_name = os.path.join(
            controllers_path(folder_controller), filename
        )

        if os.path.exists(full_path_with_name) and not self.option("force"):
            self.warning(
                f"{filename} already exists! Run the command with -f (force) to override."
            )
            return -1

        with open(full_path_with_name, "w") as f:
            f.write(content)

        file_created = os.path.join(parent_directory, filename)
        self.info(
            f"Controller Created ({controllers_path(file_created, absolute=False)})"
        )

    def get_basic_controller_path(self):
        return os.path.join(
            get_module_dir(__file__), "../stubs/controllers/Controller.py"
        )

    def get_resource_controller_path(self):
        return os.path.join(
            get_module_dir(__file__), "../stubs/controllers/ResourceController.py"
        )

    def get_api_controller_path(self):
        return os.path.join(
            get_module_dir(__file__), "../stubs/controllers/APIController.py"
        )

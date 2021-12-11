"""New Controller Command."""
from cleo import Command
import inflection
import os

from ..utils.location import controllers_path
from ..utils.filesystem import get_module_dir, render_stub_file


class MakeControllerCommand(Command):
    """
    Creates a new controller class.

    controller
        {name : Name of the controller}
        {--r|--resource : Create a "resource" controller with the usual CRUD methods}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        if not name.endswith("Controller"):
            name += "Controller"

        # create a resource controller if required
        if self.option("resource"):
            stub_path = self.get_resource_controller_path()
        else:
            stub_path = self.get_basic_controller_path()

        content = render_stub_file(stub_path, name)

        filename = f"{name}.py"
        with open(controllers_path(filename), "w") as f:
            f.write(content)

        self.info(f"Controller Created ({controllers_path(filename, absolute=False)})")

    def get_basic_controller_path(self):
        return os.path.join(
            get_module_dir(__file__), "../stubs/controllers/Controller.py"
        )

    def get_resource_controller_path(self):
        return os.path.join(
            get_module_dir(__file__), "../stubs/controllers/ResourceController.py"
        )

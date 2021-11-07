"""New Task Command """
import os
import inflection
from cleo import Command
from os.path import exists

from ...utils.filesystem import make_directory, get_module_dir, render_stub_file
from ...utils.location import base_path
from ...utils.str import as_filepath


class MakeTaskCommand(Command):
    """
    Create a new task
    task
        {name : Name of the task you want to create}
        {--d|--directory=? : Override the directory to create the task in}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        output = render_stub_file(self.get_stub_task_path(), name)

        relative_file_name = os.path.join(
            self.option("directory") or as_filepath(self.app.make("tasks.location")),
            f"{name}.py",
        )
        filepath = base_path(relative_file_name)

        if exists(relative_file_name):
            return self.line_error(
                f"Task already exists at: {relative_file_name}", style="error"
            )

        make_directory(filepath)
        with open(filepath, "w") as fp:
            fp.write(output)

        self.info(f"Task Created ({relative_file_name})")

    def get_stub_task_path(self):
        return os.path.join(get_module_dir(__file__), "../../stubs/scheduling/Task.py")

"""New Listener Command."""
from cleo import Command
import inflection
import os

from ...utils.filesystem import make_directory, get_module_dir, render_stub_file
from ...utils.str import as_filepath
from ...utils.location import base_path


class MakeListenerCommand(Command):
    """
    Creates a new listener class.

    listener
        {name : Name of the listener}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        content = render_stub_file(self.get_path(), name)

        relative_filename = os.path.join(
            as_filepath(self.app.make("listeners.location")), f"{name}.py"
        )
        filepath = base_path(relative_filename)
        make_directory(filepath)

        with open(filepath, "w") as f:
            f.write(content)
        self.info(f"Listener Created ({relative_filename})")

    def get_path(self):
        return os.path.join(get_module_dir(__file__), "../../stubs/events/Listener.py")

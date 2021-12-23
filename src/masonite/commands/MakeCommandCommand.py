"""New Command Command."""
import inflection
import os

from ..utils.location import base_path
from ..utils.filesystem import make_directory, render_stub_file, get_module_dir
from .Command import Command


class MakeCommandCommand(Command):
    """
    Creates a new command class.

    command
        {name : Name of the command}
        {--f|force=? : Force overriding file if already exists}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        if not name.endswith("Command"):
            name += "Command"

        content = render_stub_file(self.get_command_path(), name)
        relative_filename = os.path.join(
            self.app.make("commands.location"), name + ".py"
        )
        filepath = base_path(relative_filename)
        make_directory(filepath)
        if os.path.exists(filepath) and not self.option("force"):
            self.warning(
                f"{filepath} already exists! Run the command with -f (force) to override."
            )
            return -1

        with open(filepath, "w") as f:
            f.write(content)

        self.info(f"Command Created ({relative_filename})")

    def get_command_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/commands/Command.py")

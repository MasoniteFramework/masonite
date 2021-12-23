"""New Middleware Command."""
import inflection
import os

from ..utils.location import base_path
from ..utils.filesystem import get_module_dir, make_directory, render_stub_file
from .Command import Command


class MakeMiddlewareCommand(Command):
    """
    Creates a new middleware class.

    middleware
        {name : Name of the middleware}
        {--f|force=? : Force overriding file if already exists}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        if not name.endswith("Middleware"):
            name += "Middleware"

        content = render_stub_file(self.get_middleware_path(), name)

        relative_filename = os.path.join(
            self.app.make("middlewares.location"), name + ".py"
        )
        filepath = base_path(relative_filename)
        make_directory(filepath)
        if os.path.exists(relative_filename) and not self.option("force"):
            self.warning(
                f"{relative_filename} already exists! Run the command with -f (force) to override."
            )
            return -1

        with open(filepath, "w") as f:
            f.write(content)

        self.info(f"Middleware Created ({relative_filename})")

    def get_middleware_path(self):
        return os.path.join(
            get_module_dir(__file__), "../stubs/middlewares/Middleware.py"
        )

"""New View Command."""
import inflection
import os

from ..utils.location import views_path
from ..utils.filesystem import get_module_dir, render_stub_file, make_directory
from .Command import Command


class MakeViewCommand(Command):
    """
    Creates a new view.

    view
        {name : Name of the view}
        {--f|force=? : Force overriding file if already exists}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.underscore(self.argument("name"))

        content = render_stub_file(self.get_view_path(), name)

        filename = f"{name}.html"
        path = views_path(filename)
        make_directory(path)
        if os.path.exists(path) and not self.option("force"):
            self.warning(
                f"{path} already exists! Run the command with -f (force) to override."
            )
            return -1

        with open(path, "w") as f:
            f.write(content)

        self.info(f"View Created ({views_path(filename, absolute=False)})")

    def get_view_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/templates/view.html")

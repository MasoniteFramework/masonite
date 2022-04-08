"""Scaffold Auth Command."""
from shutil import copytree
import os
import sys

from ..utils.location import controllers_path, views_path, mailables_path
from ..utils.filesystem import get_module_dir
from .Command import Command


class AuthCommand(Command):
    """
    Creates a new authentication scaffold.

    auth
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        # dirs_exist_ok option is available in Python 3.8+
        # https://docs.python.org/3/library/shutil.html#shutil.copytree
        if sys.version_info.minor >= 8:
            copytree(self.get_template_path(), views_path("auth"), dirs_exist_ok=True)
            copytree(
                self.get_controllers_path(),
                controllers_path("auth"),
                dirs_exist_ok=True,
            )

            copytree(self.mailables_path(), mailables_path(), dirs_exist_ok=True)
        else:
            copytree(self.get_template_path(), views_path("auth"))
            copytree(self.get_controllers_path(), controllers_path("auth"))
            copytree(self.mailables_path(), mailables_path())

        self.info("Auth scaffolded successfully!")

    def get_template_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/templates/auth")

    def get_controllers_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/controllers/auth")

    def mailables_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/auth/mailables")

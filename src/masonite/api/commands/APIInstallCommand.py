"""Scaffold Auth Command."""
import os
from ...utils.filesystem import render_stub_file, get_module_dir
from ...utils.location import config_path
from ...utils.str import random_string


from ...commands.Command import Command


class APIInstallCommand(Command):
    """
    Adds required files for building API's

    api:install
        {--f|force=? : Force overriding file if already exists}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        stub_path = self.get_stub_config_path()

        content = render_stub_file(stub_path, "api.py")

        path = config_path("api.py")
        if os.path.exists(path) and not self.option("force"):
            self.warning(
                f"{path} already exists! Run the command with -f (force) to override."
            )
            return -1

        with open(path, "w") as f:
            f.write(content)

        if os.path.exists(path) and not self.option("force"):
            self.warning(
                f"{path} already exists! Run the command with -f (force) to override."
            )
            return -1

        with open(path, "w") as f:
            f.write(content)

        secret = random_string(25)

        self.info(f"API Installed: ({config_path('api.py', absolute=False)})")
        self.info(
            f"JWT Secret Key Is: {secret}. You should store this in an environment variable called JWT_SECRET."
        )

    def get_stub_config_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/api.py")

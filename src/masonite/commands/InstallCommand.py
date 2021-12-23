import os
import shutil
from subprocess import call

from .Command import Command


class InstallCommand(Command):
    """
    Installs all of Masonite's dependencies

    install
        {--no-key : If set, craft install command will not generate and store a new key}
        {--no-dev : If set, Masonite will install without dev dependencies}
        {--f|--force : Overwrite .env if exists}
    """

    def handle(self):

        if not os.path.isfile(".env") or self.option("force"):
            shutil.copy(".env-example", ".env")

        if os.path.isfile("Pipfile"):
            try:
                if not self.option("no-dev"):
                    call(["pipenv", "install", "--dev"])
                else:
                    call(["pipenv", "install"])

                if not self.option("no-key"):
                    call(["pipenv", "shell", "new", "key", "--store"])

                return
            except Exception:
                self.comment(
                    """Pipenv could not install from your Pipfile .. reverting to pip installing requirements.txt"""
                )
                call(["python", "-m", "pip", "install", "-r", "requirements.txt"])
        elif os.path.isfile("requirements.txt"):
            call(["python", "-m", "pip", "install", "-r", "requirements.txt"])
        else:
            raise OSError("Could not find a Pipfile or a requirements.txt file")
        if not self.option("no-key"):
            try:
                self.call("key", "--store")
            except Exception:
                self.error(
                    "Could not successfully install Masonite. This could happen for several reasons but likely because of how Masonite is installed on your system and you could be hitting permission issues when Masonite is fetching required modules."
                    " If you have correctly followed the installation instructions then you should try everything again but start inside an virtual environment first to avoid any permission issues. If that does not work then seek help in"
                    " the Masonite Slack channel. Links can be found on GitHub in the main Masonite repo."
                )

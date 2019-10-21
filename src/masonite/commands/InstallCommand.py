"""Install Command."""
import os
import shutil
import subprocess

from cleo import Command


class InstallCommand(Command):
    """
    Installs all of Masonite's dependencies.

    install
    """

    def handle(self):
        subprocess.call(["pip3", "install", "-r", "requirements.txt"])

        # create the .env file if it does not exist
        if not os.path.isfile('.env'):
            shutil.copy('.env-example', '.env')

        subprocess.call(["craft", "key", "--store"])

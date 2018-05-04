import os
import shutil
from subprocess import call

from cleo import Command


class InstallCommand(Command):
    """
    Installs all of Masonite's dependencies

    install
    """

    def handle(self):
        call(["pip3", "install", "-r", "requirements.txt"])

        # create the .env file if it does not exist
        if not os.path.isfile('.env'):
            shutil.copy('.env-example', '.env')

        call(["craft", "key", "--store"])

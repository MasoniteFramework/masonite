from cleo import Command
from subprocess import call
import os
import shutil

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

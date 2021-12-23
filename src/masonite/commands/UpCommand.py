import os

from .Command import Command


class UpCommand(Command):
    """
    Brings the server out of maintenance state.

    up
    """

    def handle(self):
        os.remove(".down")
        self.info("Server is online again !")

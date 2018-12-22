"""Up Command."""

import os

from cleo import Command


class UpCommand(Command):
    """
    Puts the sever in a maintenance state.

    up
    """

    def handle(self):
        os.remove('bootstrap/down')

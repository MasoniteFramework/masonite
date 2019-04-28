"""Up Command."""

import os

from cleo import Command


class UpCommand(Command):
    """
    Brings the server out of maintenance state.

    up
    """

    def handle(self):
        os.remove('bootstrap/down')

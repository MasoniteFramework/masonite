"""Down Command."""

from cleo import Command


class DownCommand(Command):
    """
    Puts the server in a maintenance state.

    down
    """

    def handle(self):
        with open('bootstrap/down', 'w+'):
            pass

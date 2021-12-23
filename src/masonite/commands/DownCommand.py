from .Command import Command


class DownCommand(Command):
    """
    Puts the server in a maintenance state.

    down
    """

    def handle(self):
        with open(".down", "w+"):
            pass

        self.info("Server is down for maintenance !")

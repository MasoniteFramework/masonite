"""Starts Interactive Console Command."""
import code
import sys

from cleo import Command

BANNER = """Masonite Python {} Console
This interactive console has the following things imported:
    container as 'app'

Type `exit()` to exit."""


class TinkerCommand(Command):
    """
    Run a python shell with the container pre-loaded.

    tinker
    """

    def handle(self):
        from wsgi import container

        version = "{}.{}.{}".format(
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro
        )
        banner = BANNER.format(version)

        code.interact(banner=banner, local={"app": container})

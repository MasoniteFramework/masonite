"""Craft Command.

This module is really used for backup only if the masonite CLI cannot import this for you.
This can be used by running "python craft". This module is not ran when the CLI can
successfully import commands for you.
"""

from cleo import Application
from .ProjectCommand import (
    ProjectCommand,
)

from .KeyCommand import KeyCommand
from .InstallCommand import InstallCommand

application = Application("Masonite Starter Version:", 4.0)

application.add(ProjectCommand())
application.add(KeyCommand())
application.add(InstallCommand())

if __name__ == "__main__":
    application.run()

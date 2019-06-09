"""Migrate Reset Command."""
import os
import sys

from cleo import Command
from masonite.helpers.migrations import Migrations


class MigrateResetCommand(Command):
    """
    Migrate reset.

    migrate:reset
    """

    def handle(self):
        sys.path.append(os.getcwd())
        migrations = Migrations().reset()
        self.line("")
        for notes in migrations._notes:
            self.line(notes)
        self.line("")

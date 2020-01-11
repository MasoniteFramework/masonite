"""Migrate Reset Command."""
import os
import sys

from cleo import Command
from ..helpers.migrations import Migrations


class MigrateResetCommand(Command):
    """
    Migrate reset.

    migrate:reset
        {--c|connection=default : The connection you want to run migrations on}
    """

    def handle(self):
        sys.path.append(os.getcwd())
        migrations = Migrations(self.option('connection')).reset()
        self.line("")
        for notes in migrations._notes:
            self.line(notes)
        self.line("")

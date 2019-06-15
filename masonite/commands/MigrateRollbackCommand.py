"""Migrate Rollback Command."""
import os
import sys

from cleo import Command
from masonite.helpers.migrations import Migrations


class MigrateRollbackCommand(Command):
    """
    Migrate Rollback.

    migrate:rollback
    """

    def handle(self):
        sys.path.append(os.getcwd())
        migrations = Migrations().rollback()
        self.line("")
        for notes in migrations._notes:
            self.line(notes)
        self.line("")

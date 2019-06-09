"""Migrate Reset Command."""
import os
import sys

from cleo import Command
from masonite.packages import add_venv_site_packages
from orator.exceptions.query import QueryException
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

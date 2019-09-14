"""Run Migration Command."""
import os
import sys

from cleo import Command
from masonite.helpers.migrations import Migrations


class MigrateCommand(Command):
    """
    Run migrations.

    migrate
        {--c|connection=default : The connection you want to run migrations on}
    """

    def handle(self):
        sys.path.append(os.getcwd())
        migrations = Migrations(self.option('connection')).run()
        self.line("")
        for notes in migrations._notes:
            self.line(notes)
        self.line("")

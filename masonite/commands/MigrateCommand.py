"""Run Migration Command."""
import os
import sys

from subprocess import check_output
from cleo import Command
from masonite.packages import add_venv_site_packages
from masonite.helpers.migrations import Migrations


class MigrateCommand(Command):
    """
    Run migrations.

    migrate
    """

    def handle(self):
        sys.path.append(os.getcwd())
        migrations = Migrations().run()
        self.line("")
        for notes in migrations._notes:
            self.line(notes)
        self.line("")
        
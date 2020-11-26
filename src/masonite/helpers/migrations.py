import subprocess

from ..helpers import config, HasColoredCommands
from ..packages import add_venv_site_packages
from masoniteorm.migrations import Migration


class Migrations(HasColoredCommands):
    def __init__(self, connection=None):
        self._ran = []
        self._notes = []
        from config import database

        if not connection or connection == "default":
            connection = database.DATABASES["default"]
        self.migrator = Migration("sqlite")
        self.migrator.create_table_if_not_exists()

    def run(self):
        self.migrator.migrate()

        return self

    def rollback(self):
        self.migrator.rollback()

        return self

    def refresh(self):
        self.run()
        self.rollback()

    def reset(self):
        self.migrator.rollback_all()

        return self

    def ran(self):
        return self._ran


def has_unmigrated_migrations():
    return False

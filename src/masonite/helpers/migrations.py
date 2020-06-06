import subprocess

from ..helpers import config, HasColoredCommands
from ..packages import add_venv_site_packages
from masonite.orm.migrations import Migration


class Migrations(HasColoredCommands):

    def __init__(self, connection=None):
        self._ran = []
        self._notes = []
        from config import database

        if not connection or connection == 'default':
            connection = database.DATABASES['default']
        self.migrator = Migration('sqlite')
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
    if not config('application.debug'):
        return False

    from wsgi import container
    from config.database import DB
    try:
        DB.connection()
    except Exception:
        return False

    migration_directory = ['databases/migrations']
    for key, value in container.providers.items():
        if isinstance(key, str) and 'MigrationDirectory' in key:
            migration_directory.append(value)

    for directory in migration_directory:
        try:
            output = bytes(subprocess.check_output(
                ['orator', 'migrate:status', '-c',
                    'config/database.py', '-p', directory]
            )).decode('utf-8')

            if 'No' in output:
                return True
        except Exception:
            pass

    return False

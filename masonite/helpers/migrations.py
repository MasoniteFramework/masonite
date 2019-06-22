import subprocess

from masonite.helpers import config, HasColoredCommands
from masonite.packages import add_venv_site_packages
from orator.migrations import DatabaseMigrationRepository, Migrator


class Migrations(HasColoredCommands):

    def __init__(self):
        self._ran = []
        self._notes = []
        from config import database
        self.repository = DatabaseMigrationRepository(database.DB, 'migrations')
        self.migrator = Migrator(self.repository, database.DB)
        if not self.repository.repository_exists():
            self.repository.create_repository()

        from wsgi import container

        self.migration_directories = ['databases/migrations']
        for key, value in container.providers.items():
            if isinstance(key, str) and 'MigrationDirectory' in key:
                self.migration_directories.append(value)

        try:
            add_venv_site_packages()
        except ImportError:
            self.comment(
                'This command must be ran inside of the root of a Masonite project directory')

    def run(self):
        for directory in self.migration_directories:
            try:
                if len(self.migration_directories) > 1:
                    self.info('Migrating: {}'.format(directory))
                self.migrator.run(directory)
                self._ran.append(self.repository.get_ran())
                self._notes = self.migrator._notes
            except Exception as e:
                self.danger(str(e))

        return self

    def rollback(self):
        for directory in self.migration_directories:
            try:
                if len(self.migration_directories) > 1:
                    self.info('Migrating: {}'.format(directory))
                self.migrator.rollback(directory)
                self._ran.append(self.repository.get_ran())
                self._notes = self.migrator._notes
            except Exception as e:
                self.danger(str(e))

        return self

    def refresh(self):
        self.run()
        self.rollback()

    def reset(self):
        for directory in self.migration_directories:
            try:
                if len(self.migration_directories) > 1:
                    self.info('Migrating: {}'.format(directory))
                self.migrator.reset(directory)
                self._ran.append(self.repository.get_ran())
                self._notes = self.migrator._notes
            except Exception as e:
                self.danger(str(e))

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

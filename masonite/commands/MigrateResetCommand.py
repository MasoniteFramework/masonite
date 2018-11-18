"""Migrate Reset Command."""
import os
import sys

from cleo import Command
from masonite.packages import add_venv_site_packages
from orator.exceptions.query import QueryException


class MigrateResetCommand(Command):
    """
    Migrate reset.

    migrate:reset
    """

    def handle(self):
        sys.path.append(os.getcwd())
        try:
            add_venv_site_packages()
            from wsgi import container
        except ImportError:
            self.comment(
                'This command must be ran inside of the root of a Masonite project directory')

        # Get any migration files from the Service Container
        migration_directory = ['databases/migrations']
        for key, value in container.providers.items():
            if type(key) == str and 'MigrationDirectory' in key:
                migration_directory.append(value)

        # Load in the Orator migration system
        from orator.migrations import Migrator, DatabaseMigrationRepository
        from config import database
        repository = DatabaseMigrationRepository(database.DB, 'migrations')
        migrator = Migrator(repository, database.DB)
        if not migrator.repository_exists():
            repository.create_repository()

        # Create a new list of migrations with the correct file path instead
        migration_list = []
        for migration in migrator.get_repository().get_ran():
            for directory in migration_directory:
                if os.path.exists(os.path.join(directory, migration + '.py')):
                    migration_list.append(os.path.join(os.getcwd(), directory))
                    break

        # Rollback the migrations
        notes = []
        for migration in migrator.get_repository().get_ran():
            for migration_directory in migration_list:
                try:
                    migrator.reset(migration_directory)
                except QueryException as e:
                    raise e
                except FileNotFoundError:
                    pass

                if migrator.get_notes():
                    notes += migrator.get_notes()

        # Show notes from the migrator
        self.line('')
        for note in notes:
            if not ('Nothing to rollback.' in note):
                self.line(note)
        if not notes:
            self.info('Nothing to rollback')

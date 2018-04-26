import os
import sys

from cleo import Command

from masonite.packages import add_venv_site_packages


class MigrateRollbackCommand(Command):
    """
    Migrate Rollback

    migrate:rollback
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
            if 'MigrationDirectory' in key:
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
                if os.path.exists(os.path.join(directory, migration+'.py')):
                    migration_list.append(os.path.join(os.getcwd(), directory))
                    break

        # Rollback the migrations
        for migration in migration_list:

            try:
                migrator.rollback(migration)
                for note in migrator.get_notes():
                    self.line(note)
            except Exception:
                pass

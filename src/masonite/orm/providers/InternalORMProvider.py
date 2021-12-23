from masoniteorm.commands import (
    MigrateCommand,
    MigrateRollbackCommand,
    MigrateRefreshCommand,
    MigrateResetCommand,
    MakeModelCommand,
    MakeObserverCommand,
    MigrateStatusCommand,
    MakeMigrationCommand,
    MakeSeedCommand,
    SeedRunCommand,
)

from ..commands import DbShellCommand
from ...providers import Provider
from ...utils.location import migrations_path, models_path


class ORMProvider(Provider):
    """Offical Masonite ORMProvider which configure all commands to use locations defined
    in container."""

    def __init__(self, application):
        self.application = application

    def register(self):
        models_dir = models_path(absolute=False)
        seeds_dir = self.application.make("seeds.location")
        migrations_dir = migrations_path(absolute=False)
        observers_dir = self.application.make("observers.location")
        self.application.make("commands").add(
            MakeMigrationCommand(directory=migrations_dir),
            MakeSeedCommand(directory=seeds_dir),
            MakeObserverCommand(directory=observers_dir),
            MigrateCommand(directory=migrations_dir),
            MigrateResetCommand(directory=migrations_dir),
            MakeModelCommand(directory=models_dir, migrations_directory=migrations_dir),
            MigrateStatusCommand(directory=migrations_dir),
            MigrateRefreshCommand(directory=migrations_dir, seed_directory=seeds_dir),
            MigrateRollbackCommand(directory=migrations_dir),
            SeedRunCommand(directory=seeds_dir),
            DbShellCommand(),
        )

    def boot(self):
        pass

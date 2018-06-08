from cleo import Command
import subprocess


class SeedCommand(Command):
    """
    Create a seeder to seed a database.

    seed
        {table : Name of the table to seed}
    """

    def handle(self):
        table = self.argument('table').lower()
        subprocess.call([
            "orator make:seed {}_table_seeder -p databases/seeds".format(table),
        ], shell=True)

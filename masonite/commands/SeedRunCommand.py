from cleo import Command
import subprocess


class SeedRunCommand(Command):
    """
    Create a seeder to seed a database.

    seed:run
        {table=None : Name of the table to seed}
    """

    def handle(self):
        table = self.argument('table').lower()
        if not table == 'none':
            seeder = '--seeder {}_table_seeder'.format(table.lower())
        else:
            seeder = ''

        subprocess.call([
            "orator db:seed -p databases/seeds -c config/database.py -f {}".format(seeder),
        ], shell=True)

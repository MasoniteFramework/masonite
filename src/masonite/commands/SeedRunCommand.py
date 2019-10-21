"""Run Seed Command."""
import subprocess

from cleo import Command


class SeedRunCommand(Command):
    """
    Run seed for database.

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
            "orator db:seed -p databases/seeds -c config/database.py -f {}".format(
                seeder),
        ], shell=True)

"""New Seeder Command."""
import subprocess
import os

from cleo import Command


class SeedCommand(Command):
    """
    Create a seeder to seed a database.

    seed
        {table : Name of the table to seed}
    """

    def handle(self):
        pass

"""Base Database Seeder Module."""

from orator.seeds import Seeder

from .user_table_seeder import UserTableSeeder


class DatabaseSeeder(Seeder):
    """Database Seeder Base Class."""

    def run(self):
        """Run the database seeds."""
        self.call(UserTableSeeder)

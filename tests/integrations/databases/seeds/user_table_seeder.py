"""UserTableSeeder Seeder."""

from masoniteorm.seeds import Seeder
from tests.integrations.app.User import User


class UserTableSeeder(Seeder):
    def run(self):
        """Run the database seeds."""
        User.create(
            {
                "name": "idmann509",
                "email": "idmann509@gmail.com",
                "password": "secret",
                "phone": "+123456789",
            }
        )

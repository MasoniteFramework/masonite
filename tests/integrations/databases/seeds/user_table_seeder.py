"""UserTableSeeder Seeder."""

import bcrypt
from masoniteorm.seeds import Seeder
from tests.integrations.app.User import User


def _hash(password: str) -> str:
    """Return a bcrypt hash of *password* suitable for storage."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


class UserTableSeeder(Seeder):
    def run(self):
        """Run the database seeds."""
        User.create(
            {
                "name": "Joe",
                "email": "idmann509@gmail.com",
                "password": _hash("secret"),
                "phone": "+123456789",
            }
        )

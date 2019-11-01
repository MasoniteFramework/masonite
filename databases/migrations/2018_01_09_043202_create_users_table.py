"""Migrations for creating users table."""
from orator.migrations import Migration


class CreateUsersTable(Migration):
    """Migration class for creating users table."""

    def up(self):
        """Run the migrations."""
        with self.schema.create("users") as table:
            table.increments("id")
            table.string("name")
            table.string("email").unique()
            table.string("password")
            table.string("remember_token").nullable()
            table.timestamp("verified_at").nullable()
            table.timestamps()

    def down(self):
        """Revert the migrations."""
        self.schema.drop("users")

"""TestOtherModel Migration."""

from masoniteorm.migrations import Migration


class TestOtherModel(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("test_other_models") as table:
            table.increments("id")

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("test_other_models")

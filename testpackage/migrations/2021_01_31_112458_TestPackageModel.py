"""TestPackageModel Migration."""

from masoniteorm.migrations import Migration


class TestPackageModel(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("test_package_models") as table:
            table.increments("id")

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("test_package_models")

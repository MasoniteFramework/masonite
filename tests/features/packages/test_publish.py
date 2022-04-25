import os
from tests import TestCase
from src.masonite.utils.location import migrations_path


class TestPackageProviderPublishing(TestCase):
    def test_publishing_migrations(self):
        timestamp = self.fakeTime().format("YYYY_MM_DD_HHmmss")
        self.craft(
            "package:publish", "test_package --r migrations"
        ).assertOutputContains("1_create_some_table.py").assertOutputContains(
            "2_create_other_table.py"
        )

        published_migrations = []
        dump(migrations_path())
        for migration in os.listdir(migrations_path()):
            if migration.startswith(timestamp):
                published_migrations.append(migration)

        self.assertIn(f"{timestamp}_1_create_some_table.py", published_migrations)
        self.assertIn(f"{timestamp}_2_create_other_table.py", published_migrations)

        # clean up files after publishing test migrations
        for migration in published_migrations:
            os.remove(migrations_path(migration))

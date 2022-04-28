from tests import TestCase


class TestPackageProviderPublishing(TestCase):
    def test_publishing_migrations(self):
        self.craft(
            "package:publish", "test_package --r migrations --dry"
        ).assertOutputContains("1_create_some_table.py").assertOutputContains(
            "2_create_other_table.py"
        )

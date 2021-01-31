import shutil
from os.path import isdir
from tests.packages.PackageTestCase import PackageTestCase
from testpackage.provider import package_root_path


class TestMigrations(PackageTestCase):
    @staticmethod
    def configure(self):
        # those two are mandatory
        self.name("test-package")
        self.base_path(package_root_path)
        self.add_migration("2021_01_31_112458_TestPackageModel")

    def test_add_migration(self):
        self.assertEqual(
            self.test_provider.package.migrations[0],
            "migrations/2021_01_31_112458_TestPackageModel.py",
        )

    def test_migrations_tags_is_created(self):
        self.assertIn(
            "test-package-migrations", self.test_provider._publish_migrations_tags
        )

    def test_publishing_all(self):
        self.publish_command.execute("publish TestPackageProvider")
        self.assertTrue(isdir("databases/migrations/vendor/test-package/"))
        shutil.rmtree("databases/migrations/vendor/test-package/")

    # def test_publish_migrations_only(self):
    #     self.publish_command.execute(
    #         "publish TestPackageProvider --tag test-package-migrations"
    #     )
    #     self.assertTrue(isdir("databases/migrations/vendor/test-package/"))
    #     shutil.rmtree("databases/migrations/vendor/test-package/")


class TestAdvancedMigrations(PackageTestCase):
    disable_registration = True

    def test_that_migrations_tag_can_be_overriden(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_migration(
                "2021_01_31_112458_TestPackageModel", tag="test-package-db"
            )

        self.register_test_provider(configure_override)

        self.assertIn("test-package-db", self.test_provider._publish_migrations_tags)

    def test_add_migrations(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_migrations(
                "2021_01_31_112458_TestPackageModel", "2021_01_31_123137_TestOtherModel"
            )

        self.register_test_provider(configure_override)
        self.assertIn(
            "migrations/2021_01_31_112458_TestPackageModel.py",
            self.test_provider.package.migrations,
        )
        self.assertIn(
            "migrations/2021_01_31_123137_TestOtherModel.py",
            self.test_provider.package.migrations,
        )

    def test_that_migration_file_can_be_outside_classic_location(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_migration("db.stable.2021_01_31_112458_TestPackageModel")

        self.register_test_provider(configure_override)
        self.assertIn(
            "db/stable/2021_01_31_112458_TestPackageModel.py",
            self.test_provider.package.migrations,
        )
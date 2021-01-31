import os
from tests.packages.PackageTestCase import PackageTestCase
from testpackage.provider import package_root_path
from src.masonite.helpers import load


class TestConfig(PackageTestCase):
    @staticmethod
    def configure(self):
        self.name("test-package")
        self.base_path(package_root_path)
        self.add_config("config/test.py")

    def test_name(self):
        self.assertEqual(self.test_provider.package.name, "test-package")

    def test_base_path(self):
        self.assertEqual(self.test_provider.package.base_path, package_root_path)

    def test_config(self):
        self.assertEqual(self.test_provider.package.config_name, "test")
        self.assertEqual(self.test_provider.package.config_path, "config/test.py")

    def test_config_tag_and_publish_path(self):
        self.assertIn("test-package-config", self.test_provider._publish_tags)
        publish = self.test_provider._publish_tags["test-package-config"]
        self.assertEqual(
            list(publish.values())[0],
            "config/test.py",
        )
        self.assertIn("testpackage/config/test.py", list(publish.keys())[0])

    def test_publishing_all(self):
        self.publish_command.execute("publish TestPackageProvider")
        # assert that test package config file has been created in correct location
        # by reading one of its values
        self.assertEqual(load("config.test.key"), "value")
        os.remove("config/test.py")

    def test_publish_config_only(self):
        self.publish_command.execute(
            "publish TestPackageProvider --tag test-package-config"
        )
        # assert that test package config file has been created in correct location
        # by reading one of its values
        self.assertEqual(load("config.test.key"), "value")
        os.remove("config/test.py")


class TestAdvancedConfig(PackageTestCase):
    disable_registration = True

    def test_that_published_config_name_can_be_overriden(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_config("config/test.py", "package")

        self.register_test_provider(configure_override)

        self.assertEqual(self.test_provider.package.config_name, "package")
        publish = self.test_provider._publish_tags["test-package-config"]
        self.assertEqual(list(publish.values())[0], "config/package.py")

    def test_that_config_tag_can_be_overriden(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_config("config/test.py", tag="my-package-settings")

        self.register_test_provider(configure_override)

        self.assertIn("my-package-settings", self.test_provider._publish_tags)

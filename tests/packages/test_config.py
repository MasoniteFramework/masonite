from cleo import Application
from cleo import CommandTester
import os
from tests.packages.PackageTestCase import PackageTestCase
from testpackage.provider import package_root_path
from src.masonite.commands import PublishCommand
from src.masonite.helpers import load

# class TestIncorrectConfigWithoutName(PackageTestCase):
#     @staticmethod
#     def configure(self):
#         self.base_path(package_root_path)


class TestNameAndBasePath(PackageTestCase):
    @staticmethod
    def configure(self):
        self.name("test-package")
        self.base_path(package_root_path)

    def test_name(self):
        self.assertEqual(self.test_provider.package.name, "test-package")

    def test_base_path(self):
        self.assertEqual(self.test_provider.package.base_path, package_root_path)


class TestConfig(PackageTestCase):
    def setUp(self):
        super().setUp()
        # prepare testing publishing command
        self.application = Application()
        self.application.add(PublishCommand())
        self.command = self.application.find("publish")
        self.command_tester = CommandTester(self.command)

    @staticmethod
    def configure(self):
        self.name("test-package")
        self.base_path(package_root_path)
        self.add_config("config/test.py")

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
        self.command_tester.execute("publish TestPackageProvider")
        # assert that test package config file has been created in correct location
        # by reading one of its values
        self.assertEqual(load("config.test.key"), "value")
        # TODO: does not work is it in err or output ?
        # self.assertEqual(
        #     self.command_tester.io.fetch_output(), "config/test.py has been created!"
        # )
        os.remove("config/test.py")

    # def test_publish_config_only(self):
    #     self.command_tester.execute(
    #         "publish TestPackageProvider --tag test-package-config"
    #     )
    #     # assert that test package config file has been created in correct location
    #     # by reading one of its values
    #     self.assertEqual(load("config.test.key"), "value")

    def test_config_can_be_appended(self):
        pass

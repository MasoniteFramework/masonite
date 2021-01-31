from cleo import Application

from tests.packages.PackageTestCase import PackageTestCase
from testpackage.provider import package_root_path
from testpackage.commands.demo import TestPackageDemoCommand
from testpackage.commands.other import OtherPackageCommand


class TestCommands(PackageTestCase):
    @staticmethod
    def configure(self):
        self.name("test-package")
        self.base_path(package_root_path)
        self.add_command(TestPackageDemoCommand())

    def test_add_command(self):
        self.assertIn("TestPackageDemoCommand", self.test_provider.package.commands)
        self.assertIsInstance(
            self.test_provider.package.commands["TestPackageDemoCommand"],
            TestPackageDemoCommand,
        )
        self.assertTrue(self.container.has("TestPackageDemoCommand"))

    def test_if_registered_command_can_be_executed(self):
        application = Application()
        application.add(self.container.make("TestPackageDemoCommand"))
        self.assertIsInstance(application.find("testdemo"), TestPackageDemoCommand)


class TestAdvancedCommands(PackageTestCase):
    disable_registration = True

    def test_add_command_with_given_name(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_command(TestPackageDemoCommand(), "MyPackageCommand")

        self.register_test_provider(configure_override)
        self.assertTrue(self.container.has("MyPackageCommand"))

    def test_add_command_sequentially(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_command(TestPackageDemoCommand())
            self.add_command(OtherPackageCommand())

        self.register_test_provider(configure_override)
        self.assertTrue(self.container.has("TestPackageDemoCommand"))
        self.assertTrue(self.container.has("OtherPackageCommand"))

    def test_add_commands(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_commands(OtherPackageCommand(), TestPackageDemoCommand())

        self.register_test_provider(configure_override)
        self.assertTrue(self.container.has("TestPackageDemoCommand"))
        self.assertTrue(self.container.has("OtherPackageCommand"))

from cleo import Application, CommandTester

from tests.packages.PackageTestCase import PackageTestCase
from src.masonite.providers.PackageProvider import PackageHelpCommand
from testpackage.provider import package_root_path
from testpackage.commands.demo import TestPackageDemoCommand


class TestPackageHelpCommand(PackageTestCase):
    @staticmethod
    def configure(self):
        self.name("test-package")
        self.base_path(package_root_path)
        self.add_help()
        self.add_routes("web")
        self.add_config("test")
        self.add_command(TestPackageDemoCommand(), "MyPackageCommand")
        self.add_migrations(
            "2021_01_31_112458_TestPackageModel", "2021_01_31_123137_TestOtherModel"
        )
        self.add_assets(
            {
                "package.js": "app.js",
                "package.css": None,
                "sub/admin.js": "admin.js",
            }
        )

    def test_help_command_is_registered(self):
        self.assertTrue(self.container.has("PackageHelpCommand"))

    def test_if_help_can_be_executed(self):
        application = Application()
        application.add(self.container.make("PackageHelpCommand"))
        command = application.find("packagehelp")
        self.assertIsInstance(command, PackageHelpCommand)
        self.help_command = CommandTester(command)
        self.help_command.execute("packagehelp")
        # self.assertEqual(
        #     self.help_command.io.fetch_output(), "Help for : test-package\n"
        # )
        import pdb

        pdb.set_trace()

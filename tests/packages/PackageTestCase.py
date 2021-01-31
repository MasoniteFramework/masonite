from cleo import Application
from cleo import CommandTester

from src.masonite.commands import PublishCommand
from src.masonite.testing import TestCase
from testpackage.provider import TestPackageProvider


class PackageTestCase(TestCase):
    sqlite = False
    disable_registration = False

    def setUp(self):
        super().setUp()
        # prepare testing publishing command
        self.application = Application()
        self.application.add(PublishCommand())
        self.command = self.application.find("publish")
        self.publish_command = CommandTester(self.command)
        # register package provider
        self.test_provider = TestPackageProvider()
        if not self.disable_registration:
            self.register_test_provider()

    def register_test_provider(self, configure_override=None):
        def configure():
            """swap configure method for testing behaviour"""
            if configure_override:
                configure_override(self.test_provider)
            else:
                self.configure(self.test_provider)

        self.test_provider.configure = configure
        # register provider to test behaviour
        self.test_provider.load_app(self.container).register()
        self.container.make("Providers").append(self.test_provider)
        self.container.resolve(self.test_provider.boot)

    def tearDown(self):
        super().tearDown()
        if not self.disable_registration:
            self.container.make("Providers").remove(self.test_provider)
            self.test_provider = None
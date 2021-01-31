from src.masonite.testing import TestCase
from testpackage.provider import TestPackageProvider


class PackageTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.test_provider = TestPackageProvider()

        def configure_override():
            """swap configure method for testing behaviour"""
            self.configure(self.test_provider)

        self.test_provider.configure = configure_override
        # register provider to test behaviour
        self.test_provider.load_app(self.container).register()
        self.container.make("Providers").append(self.test_provider)
        self.container.resolve(self.test_provider.boot)

    def configure(self):
        pass

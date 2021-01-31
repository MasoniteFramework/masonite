import os

from src.masonite.providers import PackageProvider

package_root_path = os.path.dirname(os.path.realpath(__file__))


class TestPackageProvider(PackageProvider):
    def configure(self):
        """This method will be overriden in the tests."""
        pass

from tests.packages.PackageTestCase import PackageTestCase
from testpackage.provider import package_root_path


class TestIncorrectUsePackageProvider(PackageTestCase):
    disable_registration = True

    def test_that_name_is_required(self):
        def configure_override(self):
            self.base_path(package_root_path)

        with self.assertRaises(NotImplementedError) as ctx:
            self.register_test_provider(configure_override)
        self.assertIn("name", str(ctx.exception))

    def test_that_base_path_is_required(self):
        def configure_override(self):
            self.name("test-package")

        with self.assertRaises(NotImplementedError) as ctx:
            self.register_test_provider(configure_override)
        self.assertIn("path", str(ctx.exception))

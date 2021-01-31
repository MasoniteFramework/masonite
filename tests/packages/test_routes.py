import os
from tests.packages.PackageTestCase import PackageTestCase
from testpackage.provider import package_root_path
from src.masonite.helpers import load


class TestRoutes(PackageTestCase):
    @staticmethod
    def configure(self):
        self.name("test-package")
        self.base_path(package_root_path)
        self.add_routes("web")

    def test_add_routes(self):
        self.assertIn("test-package-routes", self.test_provider._publish_tags)
        self.assertEqual(
            self.test_provider.package.routes,
            {"routes/web.py": "routes/vendor/test-package/web.py"},
        )

    def test_can_call_registered_routes(self):
        # self.assertEqual(self.get("/testing"))
        pass


class TestAdvancedRoutes(PackageTestCase):
    disable_registration = True

    def test_that_routestag_can_be_overriden(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_routes("web", tag="my-package-routes")

        self.register_test_provider(configure_override)

        self.assertIn("my-package-routes", self.test_provider._publish_tags)

    def test_can_add_multiple_routes(self):
        pass
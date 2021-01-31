from tests.packages.PackageTestCase import PackageTestCase
from testpackage.provider import package_root_path


class TestViews(PackageTestCase):
    @staticmethod
    def configure(self):
        self.name("test-package")
        self.base_path(package_root_path)
        self.add_views("admin", "public")

    def test_add_views(self):
        self.assertIn("test-package-views", self.test_provider._publish_tags)
        self.assertEqual(
            self.test_provider.package.views,
            {
                "templates/admin.html": "templates/vendor/test-package/admin.html",
                "templates/public.html": "templates/vendor/test-package/public.html",
            },
        )

    def test_can_render_registered_views(self):
        pass

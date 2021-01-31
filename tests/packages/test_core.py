from src.masonite.testing import TestCase
from src.masonite.providers import PackageProvider


class TestCorePackageProvider(TestCase):
    sqlite = False

    def setUp(self):
        super().setUp()
        self.package_provider = PackageProvider()

    def test_get_basename_dot(self):
        self.assertEqual(
            self.package_provider._parse_dotted_path("config"),
            ("config.py", "config.py"),
        )
        self.assertEqual(
            self.package_provider._parse_dotted_path("config.package"),
            ("config/package.py", "package.py"),
        )
        self.assertEqual(
            self.package_provider._parse_dotted_path("config.nested.package"),
            ("config/nested/package.py", "package.py"),
        )

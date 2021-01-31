import os
import shutil
from os.path import isdir, join, isfile
from tests.packages.PackageTestCase import PackageTestCase
from testpackage.provider import package_root_path


class TestAssets(PackageTestCase):
    @staticmethod
    def configure(self):
        # those two are mandatory
        self.name("test-package")
        self.base_path(package_root_path)
        self.add_asset("package.js")

    def test_add_asset(self):
        from_location = list(self.test_provider.package.assets.keys())[0]
        to_location = list(self.test_provider.package.assets.values())[0]
        self.assertEqual(to_location, "public/vendor/test-package/package.js")
        self.assertIn("resources/package.js", from_location)

    def test_assets_tags_is_created(self):
        self.assertIn("test-package-assets", self.test_provider._publish_assets_tags)

    def test_assets_are_indeed_registered(self):
        # first come masonite app files
        key = join(package_root_path, "resources/package.js")
        assets = self.container.make("staticfiles")
        self.assertIn(key, assets)
        self.assertEqual(assets[key], "public/vendor/test-package/package.js")

    def test_that_assets_can_be_published(self):
        self.publish_command.execute(
            "publish TestPackageProvider --tag test-package-assets"
        )
        created_file = "public/vendor/test-package/package.js"
        self.assertTrue(isfile(created_file))
        os.remove(created_file)


class TestAdvancedAssets(PackageTestCase):
    disable_registration = True

    def test_add_asset_with_name_override(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_asset("package.js", "app.js")

        self.register_test_provider(configure_override)

        from_location = list(self.test_provider.package.assets.keys())[0]
        to_location = list(self.test_provider.package.assets.values())[0]
        self.assertEqual(to_location, "public/vendor/test-package/app.js")
        self.assertIn("resources/package.js", from_location)

    def test_add_assets_and_name_override_and_nested_assets(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_assets(
                {
                    "package.js": "app.js",
                    "package.css": None,
                    "sub/admin.js": "admin.js",
                }
            )

        self.register_test_provider(configure_override)
        to_locations = self.test_provider.package.assets.values()
        from_locations = list(self.test_provider.package.assets.keys())
        self.assertIn("public/vendor/test-package/app.js", to_locations)
        self.assertIn("public/vendor/test-package/package.css", to_locations)
        self.assertIn("public/vendor/test-package/admin.js", to_locations)
        self.assertIn("resources/package.js", from_locations)
        self.assertIn("resources/package.css", from_locations)
        self.assertIn("resources/sub/admin.js", from_locations)

    def test_adding_assets_not_from_classic_dir(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_assets(
                {
                    "outside.js": "app.js",
                    "resources_other/style.css": None,
                }
            )

        self.register_test_provider(configure_override)
        to_locations = self.test_provider.package.assets.values()
        from_locations = list(self.test_provider.package.assets.keys())
        self.assertIn("public/vendor/test-package/app.js", to_locations)
        self.assertIn("public/vendor/test-package/style.css", to_locations)
        self.assertIn("outside.js", from_locations)
        self.assertIn("resources_other/style.css", from_locations)

    def test_that_assets_tag_can_be_overriden(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_asset("package.js", tag="package-assets")

        self.register_test_provider(configure_override)

        self.assertIn("package-assets", self.test_provider._publish_assets_tags)

    def test_that_assets_dirs_can_be_published(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_asset(
                "sub"
            )  # => ../resources/sub can be published to public/vendor/test-package/

        self.register_test_provider(configure_override)
        self.publish_command.execute(
            "publish TestPackageProvider --tag test-package-assets"
        )
        created_path = "public/vendor/test-package/sub"
        self.assertTrue(isdir(created_path))
        shutil.rmtree(created_path)

    def test_that_assets_dirs_can_be_published_to_specified_dirs(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_asset(
                "sub", "core"
            )  # => ../resources/sub can be published to public/vendor/test-package/

        self.register_test_provider(configure_override)
        self.publish_command.execute(
            "publish TestPackageProvider --tag test-package-assets"
        )
        created_path = "public/vendor/test-package/core"
        self.assertTrue(isdir(created_path))
        shutil.rmtree(created_path)

    def test_that_all_assets_can_be_published_if_in_classic_dir(self):
        def configure_override(self):
            self.name("test-package")
            self.base_path(package_root_path)
            self.add_assets()  # => ../resources/** can be published to public/vendor/test-package/

        self.register_test_provider(configure_override)
        self.publish_command.execute(
            "publish TestPackageProvider --tag test-package-assets"
        )
        created_path = "public/vendor/test-package/"
        self.assertTrue(isdir(created_path))
        self.assertTrue(isfile(join(created_path, "package.js")))
        self.assertTrue(isfile(join(created_path, "package.css")))
        self.assertTrue(isdir(join(created_path, "sub")))
        self.assertTrue(isfile(join(created_path, "sub", "admin.js")))
        shutil.rmtree(created_path)

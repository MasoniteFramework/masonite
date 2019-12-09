import shutil
import os
import filecmp

from src.masonite.commands.presets.Tailwindcss import Tailwindcss

import unittest


class TestTailwindcss(unittest.TestCase):
    def test_update_package_array(self):
        expected_packages = {
            "laravel-mix": "^4.0.14",
            "laravel-mix-purgecss": "^4.1",
            "laravel-mix-tailwind": "^0.1.0",
            "tailwindcss": "^1.0",
        }

        # Verify it works with no existing packages
        self.assertDictEqual(expected_packages, Tailwindcss().update_package_array())
        remove_packages = {
            "bootstrap": "1.2.3",
            "bootstrap-sass": "1.2.3",
            "popper.js": "1.2.3",
            "laravel-mix": "1.2.3",
            "jquery": "1.2.3",
        }
        # Verify it works to remove VueJS
        self.assertDictEqual(
            expected_packages,
            Tailwindcss().update_package_array(packages=remove_packages),
        )
        extra_packages = {
            "bootstrap": "1.2.3",
            "bootstrap-sass": "1.2.3",
            "popper.js": "1.2.3",
            "laravel-mix": "1.2.3",
            "jquery": "1.2.3",
            "dummy": "4.5.6",
        }
        expected_packages["dummy"] = "4.5.6"
        # Verify it works to remove VueJS but leaves extra packages intact
        self.assertDictEqual(
            expected_packages,
            Tailwindcss().update_package_array(packages=extra_packages),
        )

    def test_update_webpack_configuration(self):
        Tailwindcss().update_webpack_configuration()
        self.assertTrue(
            filecmp.cmp(
                "src/masonite/commands/presets/tailwindcss-stubs/webpack.mix.js",
                "webpack.mix.js",
            )
        )
        self.assertTrue(
            filecmp.cmp(
                "src/masonite/commands/presets/tailwindcss-stubs/tailwind.config.js",
                "tailwind.config.js",
            )
        )
        os.remove("webpack.mix.js")
        os.remove("tailwind.config.js")

    def test_update_styles(self):
        Tailwindcss().update_styles()
        self.assertFalse(os.path.exists("resources/sass"))
        self.assertTrue(
            filecmp.cmp(
                "src/masonite/commands/presets/tailwindcss-stubs/resources/css/app.css",
                "resources/css/app.css",
            )
        )
        shutil.rmtree("resources/css")

    def test_update_bootstrapping(self):
        Tailwindcss().update_bootstrapping()
        self.assertTrue(
            filecmp.cmp(
                "src/masonite/commands/presets/tailwindcss-stubs/resources/js/bootstrap.js",
                "resources/js/bootstrap.js",
            )
        )
        shutil.rmtree("resources/js")

    def test_install(self):
        shutil.copyfile("package.json", "package.json.save")
        Tailwindcss().install()
        self.assertTrue(
            filecmp.cmp(
                "src/masonite/commands/presets/tailwindcss-stubs/webpack.mix.js",
                "webpack.mix.js",
            )
        )
        self.assertTrue(
            filecmp.cmp(
                "src/masonite/commands/presets/tailwindcss-stubs/tailwind.config.js",
                "tailwind.config.js",
            )
        )
        shutil.rmtree("resources/js")
        shutil.rmtree("resources/css")
        os.remove("webpack.mix.js")
        os.remove("tailwind.config.js")
        shutil.copyfile("package.json.save", "package.json")
        os.remove("package.json.save")

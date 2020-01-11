import shutil
import os
import filecmp

from src.masonite.commands.presets.Bootstrap import Bootstrap

import unittest


class TestBootstrap(unittest.TestCase):

    def test_update_package_array(self):
        expected_packages = {
            'bootstrap': '^4.0.0',
            'jquery': '^3.2',
            'popper.js': '^1.12'
        }
        # Verify it works with no existing packages
        self.assertDictEqual(expected_packages, Bootstrap().update_package_array())
        extra_packages = {
            'dummy': '4.5.6'
        }
        expected_packages['dummy'] = '4.5.6'
        # Verify it works and leaves extra packages intact
        self.assertDictEqual(expected_packages, Bootstrap().update_package_array(packages=extra_packages))

    def test_update_sass(self):
        Bootstrap().update_sass()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/bootstrap-stubs/_variables.scss', 'resources/sass/_variables.scss'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/bootstrap-stubs/app.scss', 'resources/sass/app.scss'))
        shutil.rmtree('resources/sass')

    def test_install(self):
        shutil.copyfile('package.json', 'package.json.save')
        Bootstrap().install()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/bootstrap-stubs/_variables.scss', 'resources/sass/_variables.scss'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/bootstrap-stubs/app.scss', 'resources/sass/app.scss'))
        shutil.rmtree('resources/sass')
        shutil.copyfile('package.json.save', 'package.json')
        os.remove('package.json.save')

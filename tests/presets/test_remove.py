import shutil
import os
import filecmp

from src.masonite.commands.presets.Remove import Remove

import unittest


class TestRemove(unittest.TestCase):

    def test_update_package_array(self):
        expected_packages = {}
        # Verify it works with no existing packages
        self.assertDictEqual(expected_packages, Remove().update_package_array())
        removed_packages = {
            'bootstrap': '1.2.3',
            'jquery': '1.2.3',
            'popper.js': '1.2.3',
            'vue': '1.2.3',
            'vue-template-compiler': '1.2.3',
            '@babel/preset-react': '1.2.3',
            'react': '1.2.3',
            'react-dom': '1.2.3'
        }
        # Verify it works to remove Vue, React, and Bootstrap
        self.assertDictEqual(expected_packages, Remove().update_package_array(packages=removed_packages))
        extra_packages = {
            'bootstrap': '1.2.3',
            'jquery': '1.2.3',
            'popper.js': '1.2.3',
            'vue': '1.2.3',
            'vue-template-compiler': '1.2.3',
            '@babel/preset-react': '1.2.3',
            'react': '1.2.3',
            'react-dom': '1.2.3',
            'dummy': '4.5.6'
        }
        expected_packages['dummy'] = '4.5.6'
        # Verify it works to remove Vue, React, and Bootstrap but leaves extra packages intact
        self.assertDictEqual(expected_packages, Remove().update_package_array(packages=extra_packages))

    def test_update_webpack_configuration(self):
        Remove().update_webpack_configuration()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/remove-stubs/webpack.mix.js', 'webpack.mix.js'))
        os.remove('webpack.mix.js')

    def test_update_bootstrapping(self):
        Remove().update_bootstrapping()
        self.assertTrue(os.path.exists('resources/sass/app.scss'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/remove-stubs/app.js', 'resources/js/app.js'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/remove-stubs/bootstrap.js', 'resources/js/bootstrap.js'))
        shutil.rmtree('resources/js')
        shutil.rmtree('resources/sass')

    def test_install(self):
        shutil.copyfile('package.json', 'package.json.save')
        Remove().install()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/remove-stubs/webpack.mix.js', 'webpack.mix.js'))
        self.assertTrue(os.path.exists('resources/sass/app.scss'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/remove-stubs/app.js', 'resources/js/app.js'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/remove-stubs/bootstrap.js', 'resources/js/bootstrap.js'))
        self.assertFalse(os.path.exists('resources/sass/_variables.scss'))
        self.assertFalse(os.path.exists('resources/js/components'))
        self.assertFalse(os.path.exists('public/css'))
        self.assertFalse(os.path.exists('public/js'))
        shutil.rmtree('resources/js')
        shutil.rmtree('resources/sass')
        os.remove('webpack.mix.js')
        shutil.copyfile('package.json.save', 'package.json')
        os.remove('package.json.save')

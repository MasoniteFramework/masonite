import shutil
import os
import filecmp

from src.masonite.commands.presets.React import React

import unittest


class TestReact(unittest.TestCase):

    def test_update_package_array(self):
        expected_packages = {
            '@babel/preset-react': '^7.0.0',
            'react': '^16.2.0',
            'react-dom': '^16.2.0'
        }
        # Verify it works with no existing packages
        self.assertDictEqual(expected_packages, React().update_package_array())
        vue_packages = {
            'vue': '1.2.3'
        }
        # Verify it works to remove VueJS
        self.assertDictEqual(expected_packages, React().update_package_array(packages=vue_packages))
        extra_packages = {
            'vue': '1.2.3',
            'dummy': '4.5.6'
        }
        expected_packages['dummy'] = '4.5.6'
        # Verify it works to remove VueJS but leaves extra packages intact
        self.assertDictEqual(expected_packages, React().update_package_array(packages=extra_packages))

    def test_update_webpack_configuration(self):
        React().update_webpack_configuration()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/react-stubs/webpack.mix.js', 'webpack.mix.js'))
        os.remove('webpack.mix.js')

    def test_update_component(self):
        React().ensure_component_directory_exists()
        React().update_component()
        vue_component = 'resources/js/components/ExampleComponent.vue'
        self.assertFalse(os.path.exists(vue_component))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/react-stubs/Example.js', 'resources/js/components/Example.js'))
        shutil.rmtree('resources/js')

    def test_update_bootstrapping(self):
        React().ensure_component_directory_exists()
        React().update_bootstrapping()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/react-stubs/app.js', 'resources/js/app.js'))
        shutil.rmtree('resources/js')

    def test_install(self):
        shutil.copyfile('package.json', 'package.json.save')
        React().install()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/react-stubs/webpack.mix.js', 'webpack.mix.js'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/react-stubs/Example.js', 'resources/js/components/Example.js'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/react-stubs/app.js', 'resources/js/app.js'))
        self.assertTrue(os.path.exists('resources/sass/app.scss'))
        shutil.rmtree('resources/sass')
        shutil.rmtree('resources/js')
        os.remove('webpack.mix.js')
        shutil.copyfile('package.json.save', 'package.json')
        os.remove('package.json.save')

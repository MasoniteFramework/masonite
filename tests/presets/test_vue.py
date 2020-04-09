import shutil
import os
import filecmp

from src.masonite.commands.presets.Vue import Vue

import unittest


class TestVue(unittest.TestCase):

    def test_update_package_array(self):
        expected_packages = {
            'vue': '^2.5.17'
        }
        # Verify it works with no existing packages
        self.assertDictEqual(expected_packages, Vue().update_package_array())
        react_packages = {
            'react': '1.2.3'
        }
        # Verify it works to remove React
        self.assertDictEqual(expected_packages, Vue().update_package_array(packages=react_packages))
        extra_packages = {
            'react': '1.2.3',
            'dummy': '4.5.6'
        }
        expected_packages['dummy'] = '4.5.6'
        # Verify it works to remove React but leaves extra packages intact
        self.assertDictEqual(expected_packages, Vue().update_package_array(packages=extra_packages))

    def test_update_webpack_configuration(self):
        Vue().update_webpack_configuration()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue-stubs/webpack.mix.js', 'webpack.mix.js'))
        os.remove('webpack.mix.js')

    def test_update_component(self):
        Vue().ensure_component_directory_exists()
        Vue().update_component()
        vue_component = 'resources/js/components/Example.js'
        self.assertFalse(os.path.exists(vue_component))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue-stubs/ExampleComponent.vue', 'resources/js/components/ExampleComponent.vue'))
        shutil.rmtree('resources/js')

    def test_update_bootstrapping(self):
        Vue().ensure_component_directory_exists()
        Vue().update_bootstrapping()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue-stubs/app.js', 'resources/js/app.js'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/shared-stubs/bootstrap.js', 'resources/js/bootstrap.js'))
        shutil.rmtree('resources/js')

    def test_install(self):
        shutil.copyfile('package.json', 'package.json.save')
        Vue().install()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue-stubs/webpack.mix.js', 'webpack.mix.js'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue-stubs/ExampleComponent.vue', 'resources/js/components/ExampleComponent.vue'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue-stubs/app.js', 'resources/js/app.js'))
        shutil.rmtree('resources/js')
        os.remove('webpack.mix.js')
        shutil.copyfile('package.json.save', 'package.json')
        os.remove('package.json.save')

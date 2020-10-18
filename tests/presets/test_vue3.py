import shutil
import os
import filecmp
import unittest

from src.masonite.commands.presets.Vue3 import Vue3


class TestVue(unittest.TestCase):

    def test_update_package_array(self):
        expected_packages = {
            'vue': '^3.0.0',
            '@vue/compiler-sfc': '^3.0.0',
            'laravel-mix': '^6.0.0-beta.7',
            'vue-loader': '^16.0.0-beta.8',
            'postcss': '^8.1.1'
        }
        # Verify it works with no existing packages
        self.assertDictEqual(expected_packages, Vue3().update_package_array())
        react_packages = {
            'react': '1.2.3'
        }
        # Verify it works to remove React
        self.assertDictEqual(expected_packages, Vue3().update_package_array(packages=react_packages))
        extra_packages = {
            'react': '1.2.3',
            'dummy': '4.5.6'
        }
        expected_packages['dummy'] = '4.5.6'
        # Verify it works to remove React but leaves extra packages intact
        self.assertDictEqual(expected_packages, Vue3().update_package_array(packages=extra_packages))

    def test_update_webpack_configuration(self):
        Vue3().update_webpack_configuration()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue3-stubs/webpack.mix.js', 'webpack.mix.js'))
        os.remove('webpack.mix.js')

    def test_update_component(self):
        Vue3().ensure_component_directory_exists()
        Vue3().update_component()
        react_component = 'resources/js/components/Example.js'
        self.assertFalse(os.path.exists(react_component))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue3-stubs/HelloWorld.vue', 'resources/js/components/HelloWorld.vue'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue3-stubs/App.vue', 'resources/js/App.vue'))
        shutil.rmtree('resources/js')

    def test_update_bootstrapping(self):
        Vue3().ensure_component_directory_exists()
        Vue3().update_bootstrapping()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue3-stubs/app.js', 'resources/js/app.js'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/shared-stubs/bootstrap.js', 'resources/js/bootstrap.js'))
        shutil.rmtree('resources/js')

    def test_create_view(self):
        Vue3().create_view()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue3-stubs/app.html', 'resources/templates/app_vue3.html'))
        os.remove('resources/templates/app_vue3.html')

    def test_install(self):
        shutil.copyfile('package.json', 'package.json.save')
        Vue3().install()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue3-stubs/webpack.mix.js', 'webpack.mix.js'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue3-stubs/HelloWorld.vue', 'resources/js/components/HelloWorld.vue'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue3-stubs/App.vue', 'resources/js/App.vue'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue3-stubs/app.js', 'resources/js/app.js'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/vue3-stubs/app.html', 'resources/templates/app_vue3.html'))
        self.assertTrue(os.path.exists('resources/sass/app.scss'))
        shutil.rmtree('resources/sass')
        shutil.rmtree('resources/js')
        os.remove('resources/templates/app_vue3.html')
        os.remove('webpack.mix.js')
        shutil.copyfile('package.json.save', 'package.json')
        os.remove('package.json.save')

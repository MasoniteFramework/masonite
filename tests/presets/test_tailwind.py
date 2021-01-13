import shutil
import os
import filecmp
import unittest

from src.masonite.commands.presets.Tailwind import Tailwind


class TestTailwind(unittest.TestCase):

    def test_update_package_array(self):
        expected_packages = {
            'tailwindcss': '^2.0.2',
            'autoprefixer': '^10.2.1',
        }
        # Verify it works with no existing packages
        self.assertDictEqual(expected_packages, Tailwind().update_package_array())

    def test_update_webpack_configuration(self):
        Tailwind().update_webpack_configuration()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/tailwind-stubs/webpack.mix.js', 'webpack.mix.js'))
        os.remove('webpack.mix.js')

    def test_create_tailwind_config(self):
        Tailwind().create_tailwind_config()
        config_file = 'tailwind.config.js'
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/tailwind-stubs/tailwind.config.js', 'tailwind.config.js'))
        os.remove('tailwind.config.js')

    def test_install(self):
        shutil.copyfile('package.json', 'package.json.save')
        shutil.copyfile('storage/static/sass/style.scss', 'style.scss.save')
        shutil.copyfile('resources/templates/base.html', 'base.html.save')
        shutil.copyfile('resources/templates/welcome.html', 'welcome.html.save')
        Tailwind().install()
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/Tailwind-stubs/webpack.mix.js', 'webpack.mix.js'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/Tailwind-stubs/tailwind.config.js', 'tailwind.config.js'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/Tailwind-stubs/style.scss', 'storage/static/sass/style.scss'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/Tailwind-stubs/base.html', 'resources/templates/base.html'))
        self.assertTrue(filecmp.cmp('src/masonite/commands/presets/Tailwind-stubs/welcome.html', 'resources/templates/welcome.html'))
        os.remove('tailwind.config.js')
        os.remove('webpack.mix.js')
        shutil.copyfile('package.json.save', 'package.json')
        os.remove('package.json.save')
        shutil.copyfile('style.scss.save', 'storage/static/sass/style.scss')
        os.remove('style.scss.save')
        shutil.copyfile('base.html.save', 'resources/templates/base.html')
        os.remove('base.html.save')
        shutil.copyfile('welcome.html.save', 'resources/templates/welcome.html')
        os.remove('welcome.html.save')

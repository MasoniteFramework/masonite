"""Remove Preset"""
import os
import shutil
from ..presets import Preset


class Remove(Preset):
    """Removes any defined Preset"""

    def install(self):
        """Install the preset"""
        self.update_packages()
        self.update_bootstrapping()
        self.update_webpack_configuration()
        self.remove_node_modules()
        if os.path.exists(os.path.realpath('resources/sass/_variables.scss')):
            os.remove('resources/sass/_variables.scss')
        shutil.rmtree('resources/js/components', ignore_errors=True)
        shutil.rmtree('public/css', ignore_errors=True)
        shutil.rmtree('public/js', ignore_errors=True)

    def update_package_array(self, packages={}):
        """Updates the packages array to remove React, VueJS, and Bootstrap packages"""
        packages_to_remove = [
            'bootstrap',
            'jquery',
            'popper.js',
            'vue',
            'vue-template-compiler',
            '@babel/preset-react',
            'react',
            'react-dom'
        ]
        for package in packages_to_remove:
            packages.pop(package, None)

        return packages

    def update_webpack_configuration(self):
        """Copy webpack.mix.js file into application"""
        shutil.copyfile('src/masonite/commands/presets/remove-stubs/webpack.mix.js', 'webpack.mix.js')

    def update_bootstrapping(self):
        """Copies template app.js file into application"""
        with open('resources/sass/app.scss', 'w') as f:
            f.write('')
        shutil.copyfile('src/masonite/commands/presets/remove-stubs/app.js', 'resources/js/app.js')
        shutil.copyfile('src/masonite/commands/presets/remove-stubs/bootstrap.js', 'resources/js/bootstrap.js')

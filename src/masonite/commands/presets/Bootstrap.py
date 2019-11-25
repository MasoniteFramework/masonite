"""Bootstrap Preset"""
import os
import shutil
from ..presets import Preset


class Bootstrap(Preset):
    """Configure the front-end scaffolding for the application to use Bootstrap"""

    def install(self):
        """Install the preset"""
        self.update_packages()
        self.update_sass()
        self.remove_node_modules()

    def update_package_array(self, packages={}):
        """Updates the packages array to include Bootstrap specific packages"""
        packages['bootstrap'] = '^4.0.0'
        packages['jquery'] = '^3.2'
        packages['popper.js'] = '^1.12'
        return packages

    def update_sass(self):
        """Copies Bootstrap scss files into application"""
        directory = 'resources/sass'
        if not os.path.exists(os.path.realpath(directory)):
            os.makedirs(os.path.realpath(directory))
        shutil.copyfile(os.path.dirname(__file__) + '/bootstrap-stubs/_variables.scss', 'resources/sass/_variables.scss')
        shutil.copyfile(os.path.dirname(__file__) + '/bootstrap-stubs/app.scss', 'resources/sass/app.scss')

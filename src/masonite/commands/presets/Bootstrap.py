import os
import shutil
from ..presets import Preset

class Bootstrap(Preset):

    def install(self):
        """
        Install the preset
        """
        self.updatePackages()
        self.updateSass()
        self.removeNodeModules()

    def updatePackageArray(self, packages: {}):
        packages['bootstrap'] = '^4.0.0'
        packages['jquery'] = '^3.2'
        packages['popper.js'] = '^1.12'
        return packages

    def updateSass(self):
        directory = 'resources/sass'
        if not os.path.exists(os.path.realpath(directory)):
            os.makedirs(os.path.realpath(directory))
        shutil.copyfile('src/masonite/commands/presets/bootstrap-stubs/_variables.scss', 'resources/sass/_variables.scss')
        shutil.copyfile('src/masonite/commands/presets/bootstrap-stubs/app.scss', 'resources/sass/app.scss')

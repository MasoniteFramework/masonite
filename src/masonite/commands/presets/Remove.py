import os
import shutil
from ..presets import Preset

class Remove(Preset):

    def install(self):
        """
        Install the preset
        """
        self.updatePackages()
        self.updateBootstrapping()
        self.updateWebpackConfiguration()
        self.removeNodeModules()
        if (os.path.exists(os.path.realpath('resources/sass/_variables.scss'))):
            os.remove('resources/sass/_variables.scss')
        shutil.rmtree('resources/js/components', ignore_errors=True)
        shutil.rmtree('public/css', ignore_errors=True)
        shutil.rmtree('public/js', ignore_errors=True)

    def updatePackageArray(self, packages: {}):
        packagesToRemove = [
            'bootstrap',
            'jquery',
            'popper.js',
            'vue',
            'vue-template-compiler',
            '@babel/preset-react',
            'react',
            'react-dom'
        ]
        for package in packagesToRemove:
            packages.pop(package, None)

        return packages

    def updateWebpackConfiguration(self):
        shutil.copyfile('src/masonite/commands/presets/remove-stubs/webpack.mix.js', 'webpack.mix.js')

    def updateBootstrapping(self):
        with open('resources/sass/app.scss', 'w') as f:
            f.write('')
        shutil.copyfile('src/masonite/commands/presets/remove-stubs/app.js', 'resources/js/app.js')
        shutil.copyfile('src/masonite/commands/presets/remove-stubs/bootstrap.js', 'resources/js/bootstrap.js')

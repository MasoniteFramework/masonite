import os
import shutil
from ..presets import Preset

class Vue(Preset):

    def install(self):
        """
        Install the preset
        """
        self.ensureComponentDirectoryExists()
        self.updatePackages()
        self.updateWebpackConfiguration()
        self.updateBootstrapping()
        self.updateComponent()
        self.removeNodeModules()

    def updatePackageArray(self, packages: {}):
        for package in ['@babel/preset-react', 'react', 'react-dom']:
            packages.pop(package, None)

        packages['vue'] = '^2.5.17'
        return packages

    def updateWebpackConfiguration(self):
        shutil.copyfile('src/masonite/commands/presets/vue-stubs/webpack.mix.js', 'webpack.mix.js')

    def updateComponent(self):
        vueComponent = 'resources/js/components/Example.js'
        if (os.path.exists(os.path.realpath(vueComponent))):
            os.remove(vueComponent)
        shutil.copyfile('src/masonite/commands/presets/vue-stubs/ExampleComponent.vue', 'resources/js/components/ExampleComponent.vue')

    def updateBootstrapping(self):
        shutil.copyfile('src/masonite/commands/presets/vue-stubs/app.js', 'resources/js/app.js')

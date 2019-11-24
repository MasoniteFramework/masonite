import os
import shutil
from ..presets import Preset

class React(Preset):

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
        for package in ['vue', 'vue-template-compiler']:
            packages.pop(package, None)

        packages['@babel/preset-react'] = '^7.0.0'
        packages['react'] = '^16.2.0'
        packages['react-dom'] = '^16.2.0'
        return packages

    def updateWebpackConfiguration(self):
        shutil.copyfile('src/masonite/commands/presets/react-stubs/webpack.mix.js', 'webpack.mix.js')

    def updateComponent(self):
        vueComponent = 'resources/js/components/ExampleComponent.vue'
        if (os.path.exists(os.path.realpath(vueComponent))):
            os.remove(vueComponent)
        shutil.copyfile('src/masonite/commands/presets/react-stubs/Example.js', 'resources/js/components/Example.js')

    def updateBootstrapping(self):
        shutil.copyfile('src/masonite/commands/presets/react-stubs/app.js', 'resources/js/app.js')

import os
import shutil
from ..presets import Preset


class Vue(Preset):

    def install(self):
        """Install the preset"""
        self.ensure_component_directory_exists()
        self.update_packages()
        self.update_webpack_configuration()
        self.update_bootstrapping()
        self.update_component()
        self.remove_node_modules()

    def update_package_array(self, packages: {}):
        for package in ['@babel/preset-react', 'react', 'react-dom']:
            packages.pop(package, None)

        packages['vue'] = '^2.5.17'
        return packages

    def update_webpack_configuration(self):
        shutil.copyfile('src/masonite/commands/presets/vue-stubs/webpack.mix.js', 'webpack.mix.js')

    def update_component(self):
        vue_component = 'resources/js/components/Example.js'
        if os.path.exists(os.path.realpath(vue_component)):
            os.remove(vue_component)
        shutil.copyfile('src/masonite/commands/presets/vue-stubs/ExampleComponent.vue', 'resources/js/components/ExampleComponent.vue')

    def update_bootstrapping(self):
        shutil.copyfile('src/masonite/commands/presets/vue-stubs/app.js', 'resources/js/app.js')

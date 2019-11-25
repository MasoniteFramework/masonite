import os
import shutil
from ..presets import Preset


class React(Preset):

    def install(self):
        """Install the preset"""
        self.ensure_component_directory_exists()
        self.update_packages()
        self.update_webpack_configuration()
        self.update_bootstrapping()
        self.update_component()
        self.remove_node_modules()

    def update_package_array(self, packages: {}):
        for package in ['vue', 'vue-template-compiler']:
            packages.pop(package, None)

        packages['@babel/preset-react'] = '^7.0.0'
        packages['react'] = '^16.2.0'
        packages['react-dom'] = '^16.2.0'
        return packages

    def update_webpack_configuration(self):
        shutil.copyfile('src/masonite/commands/presets/react-stubs/webpack.mix.js', 'webpack.mix.js')

    def update_component(self):
        vue_component = 'resources/js/components/ExampleComponent.vue'
        if os.path.exists(os.path.realpath(vue_component)):
            os.remove(vue_component)
        shutil.copyfile('src/masonite/commands/presets/react-stubs/Example.js', 'resources/js/components/Example.js')

    def update_bootstrapping(self):
        shutil.copyfile('src/masonite/commands/presets/react-stubs/app.js', 'resources/js/app.js')

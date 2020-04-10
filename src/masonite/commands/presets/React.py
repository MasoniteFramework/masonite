"""React Preset"""
import os
import shutil
from ..presets import Preset


class React(Preset):
    """
    Configure the front-end scaffolding for the application to use React

    Will also remove VueJS as React and Vue are a bit mutally exclusive
    """

    def install(self):
        """Install the preset"""
        self.ensure_component_directory_exists()
        self.update_packages()
        self.update_webpack_configuration()
        self.update_bootstrapping()
        self.update_component()
        self.create_scss_file()
        self.remove_node_modules()

    def update_package_array(self, packages={}):
        """
        Updates the packages array to include React specific packages
        but also remove VueJS ones
        """
        for package in ['vue', 'vue-template-compiler']:
            packages.pop(package, None)

        packages['@babel/preset-react'] = '^7.0.0'
        packages['react'] = '^16.2.0'
        packages['react-dom'] = '^16.2.0'
        return packages

    def update_webpack_configuration(self):
        """Copy webpack.mix.js file into application"""
        shutil.copyfile(os.path.dirname(__file__) + '/react-stubs/webpack.mix.js', 'webpack.mix.js')

    def update_component(self):
        """
        Copy example React component into application
        (delete example Vue component if it exists)
        """
        vue_component = 'resources/js/components/ExampleComponent.vue'
        if os.path.exists(os.path.realpath(vue_component)):
            os.remove(vue_component)
        shutil.copyfile(os.path.dirname(__file__) + '/react-stubs/Example.js', 'resources/js/components/Example.js')

    def update_bootstrapping(self):
        """Copies template app.js and bootstrap.js into application"""
        shutil.copyfile(os.path.dirname(__file__) + '/react-stubs/app.js', 'resources/js/app.js')
        shutil.copyfile(os.path.dirname(__file__) + '/shared-stubs/bootstrap.js', 'resources/js/bootstrap.js')

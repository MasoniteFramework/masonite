"""Vue 3 Preset"""
import os
import shutil
from ..presets import Preset


class Vue3(Preset):
    """
    Configure the front-end scaffolding for the application to use VueJS 3.0

    Will also remove React as React and Vue are a bit mutally exclusive
    """

    def install(self):
        """Install the preset"""
        self.ensure_component_directory_exists()
        self.update_packages()
        self.update_webpack_configuration()
        self.update_bootstrapping()
        self.update_component()
        self.create_scss_file()
        self.create_view()
        self.remove_node_modules()

    def update_package_array(self, packages={}):
        """
        Updates the packages array to include VueJS specific packages
        but also remove React ones
        """
        for package in ["@babel/preset-react", "react", "react-dom"]:
            packages.pop(package, None)

        packages["vue"] = "^3.0.4"
        packages["@vue/compiler-sfc"] = "^3.0.4"
        packages["vue-loader"] = "^16.1.2"

        return packages

    def update_webpack_configuration(self):
        """Copy webpack.mix.js file into application"""
        shutil.copyfile(
            os.path.dirname(__file__) + "/vue3-stubs/webpack.mix.js", "webpack.mix.js"
        )

    def update_component(self):
        """
        Copy example VueJS component into application
        (delete example React component if it exists)
        """
        # delete React component if exists
        vue_component = "resources/js/components/Example.js"
        if os.path.exists(os.path.realpath(vue_component)):
            os.remove(vue_component)

        shutil.copyfile(
            os.path.dirname(__file__) + "/vue3-stubs/HelloWorld.vue",
            os.path.join("resources/js/components/", "HelloWorld.vue"),
        )
        shutil.copyfile(
            os.path.dirname(__file__) + "/vue3-stubs/App.vue",
            os.path.join("resources/js/", "App.vue"),
        )

    def update_bootstrapping(self):
        """Copies template app.js and bootstrap.js into application"""
        shutil.copyfile(
            os.path.dirname(__file__) + "/vue3-stubs/app.js", "resources/js/app.js"
        )
        shutil.copyfile(
            os.path.dirname(__file__) + "/shared-stubs/bootstrap.js",
            "resources/js/bootstrap.js",
        )

    def create_view(self):
        """Copy an example app view with assets included"""
        shutil.copyfile(
            os.path.dirname(__file__) + "/vue3-stubs/app.html",
            "resources/templates/app_vue3.html",
        )

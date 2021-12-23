"""Vue 3 Preset"""
import shutil
import os

from .Preset import Preset
from ..utils.filesystem import make_directory
from ..utils.location import resources_path, views_path


class Vue(Preset):
    """
    Configure the front-end scaffolding for the application to use VueJS 3.0

    Will also remove React as React and Vue are a bit mutally exclusive
    """

    key = "vue"
    packages = {"vue": "^3.2.26", "vue-loader": "^16.8.3"}
    removed_packages = ["@babel/preset-react", "react", "react-dom"]

    def install(self):
        """Install the preset"""
        self.update_packages(dev=True)
        self.update_webpack_mix()
        self.update_js()
        self.add_components()
        self.update_css()
        self.create_view()
        self.remove_node_modules()

    def add_components(self):
        """Copy example VueJS component into application (delete example React component
        if it exists)"""
        # make components directory if does not exists
        make_directory(resources_path("js/components/HelloWorld.vue"))

        # delete React component if exists
        react_file = resources_path("js/components/Example.js")
        if os.path.exists(react_file):
            os.remove(react_file)

        # add Vue components
        shutil.copyfile(
            self.get_template_path("HelloWorld.vue"),
            resources_path("js/components/HelloWorld.vue"),
        )
        shutil.copyfile(self.get_template_path("App.vue"), resources_path("js/App.vue"))

    def create_view(self):
        """Copy an example app view with assets included."""
        shutil.copyfile(self.get_template_path("app.html"), views_path("app_vue3.html"))

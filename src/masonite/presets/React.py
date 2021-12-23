"""React Preset"""
import shutil
import os

from .Preset import Preset
from ..utils.filesystem import make_directory
from ..utils.location import resources_path, views_path


class React(Preset):
    """
    Configure the front-end scaffolding for the application to use ReactJS

    Will also remove Vue as Vue and React are a bit mutally exclusive
    """

    key = "react"
    packages = {
        "react": "^17.0.2",
        "react-dom": "^17.0.2",
        "@babel/preset-react": "^7.16.5",
    }
    removed_packages = ["vue", "vue-loader"]

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
        """Copy example React component into application (delete example Vue component
        if it exists)"""
        # make components directory if does not exists
        make_directory(resources_path("js/components/Example.js"))

        # delete Vue components if exists
        vue_files = [
            resources_path("js/components/HelloWorld.vue"),
            resources_path("js/App.vue"),
        ]
        for vue_file in vue_files:
            if os.path.exists(vue_file):
                os.remove(vue_file)

        # add Vue components
        shutil.copyfile(
            self.get_template_path("Example.js"),
            resources_path("js/components/Example.js"),
        )

    def create_view(self):
        """Copy an example app view with assets included."""
        shutil.copyfile(
            self.get_template_path("app.html"), views_path("app_react.html")
        )

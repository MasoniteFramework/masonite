"""Tailwind Preset"""
import os
import shutil
from ..presets import Preset


class Tailwind(Preset):
    """
    Configure the front-end scaffolding for the application to use Tailwind
    """

    def install(self):
        """Install the preset"""
        self.update_packages()
        self.update_webpack_configuration()
        self.create_tailwind_config()
        self.update_scss_file()
        self.update_base_views()
        self.remove_node_modules()

    def update_package_array(self, packages={}):
        """
        Updates the packages array to include VueJS specific packages
        """
        packages["autoprefixer"] = "^10.2.1"
        packages["tailwindcss"] = "^2.0.2"
        return packages

    def update_webpack_configuration(self):
        """Copy webpack.mix.js file into application"""
        shutil.copyfile(
            os.path.dirname(__file__) + "/tailwind-stubs/webpack.mix.js",
            "webpack.mix.js",
        )

    def create_tailwind_config(self):
        """
        Copy example Tailwind configuration into application
        """
        shutil.copyfile(
            os.path.dirname(__file__) + "/tailwind-stubs/tailwind.config.js",
            "tailwind.config.js",
        )

    def update_scss_file(self):
        """Create a app.scss file configured for Tailwind."""
        shutil.copyfile(
            os.path.dirname(__file__) + "/tailwind-stubs/style.scss",
            "storage/static/sass/style.scss",
        )

    def update_base_views(self):
        """Update base views"""
        shutil.copyfile(
            os.path.dirname(__file__) + "/tailwind-stubs/base.html",
            "resources/templates/base.html",
        )
        shutil.copyfile(
            os.path.dirname(__file__) + "/tailwind-stubs/welcome.html",
            "resources/templates/welcome.html",
        )

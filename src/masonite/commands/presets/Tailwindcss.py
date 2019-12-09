"""Tailwind CSS Preset"""
import os
import shutil
from ..presets import Preset


class Tailwindcss(Preset):
    """Configure the front-end scaffolding for the application to use Tailwind CSS"""

    def install(self):
        """Install the preset"""
        self.update_packages()
        self.update_webpack_configuration()
        self.update_bootstrapping()
        self.update_styles()
        self.remove_node_modules()

    def update_package_array(self, packages={}):
        """Updates the packages array to include Tailwind CSS specific packages"""
        for package in [
            "bootstrap",
            "bootstrap-sass",
            "popper.js",
            "laravel-mix",
            "jquery",
        ]:
            packages.pop(package, None)

        packages["laravel-mix"] = "^4.0.14"
        packages["laravel-mix-purgecss"] = "^4.1"
        packages["laravel-mix-tailwind"] = "^0.1.0"
        packages["tailwindcss"] = "^1.0"
        return packages

    def update_webpack_configuration(self):
        """Copy webpack.mix.js file into application"""
        shutil.copyfile(
            os.path.dirname(__file__) + "/tailwindcss-stubs/webpack.mix.js",
            "webpack.mix.js",
        )
        shutil.copyfile(
            os.path.dirname(__file__) + "/tailwindcss-stubs/tailwind.config.js",
            "tailwind.config.js",
        )

    def update_styles(self):
        """Update CSS files"""
        shutil.rmtree("resources/sass/", ignore_errors=True)
        directory = "resources/css"
        if not os.path.exists(os.path.realpath(directory)):
            os.makedirs(os.path.realpath(directory))
        shutil.copyfile(
            os.path.dirname(__file__) + "/tailwindcss-stubs/resources/css/app.css",
            "resources/css/app.css",
        )

    def update_bootstrapping(self):
        """Copies template app.js file into application"""
        directory = "resources/js"
        if not os.path.exists(os.path.realpath(directory)):
            os.makedirs(os.path.realpath(directory))
        shutil.copyfile(
            os.path.dirname(__file__) + "/tailwindcss-stubs/resources/js/bootstrap.js",
            "resources/js/bootstrap.js",
        )

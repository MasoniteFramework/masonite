"""Tailwind Preset"""
import shutil

from ..utils.filesystem import make_full_directory
from ..utils.location import base_path, resources_path
from .Preset import Preset


class Tailwind(Preset):
    """
    Configure the front-end scaffolding for the application to use Tailwind
    """

    key = "tailwind"
    packages = {"tailwindcss": "^3.0.7", "postcss": "^8.4.5", "autoprefixer": "^10.4.0"}

    def install(self):
        """Install the preset"""
        self.update_packages(dev=True)
        self.update_webpack_mix()
        self.add_tailwind_config()
        self.update_css()
        self.remove_node_modules()

    def add_tailwind_config(self):
        """Copy example Tailwind configuration into application."""
        shutil.copyfile(
            self.get_template_path("tailwind.config.js"),
            base_path("tailwind.config.js"),
        )

    def update_css(self):
        """Create/Override an app.css file configured for the preset."""
        make_full_directory(resources_path("css"))
        shutil.copyfile(
            self.get_template_path("app.css"), resources_path("css/app.css")
        )

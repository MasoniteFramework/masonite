"""Bootstrap Preset"""
import shutil

from ..utils.location import resources_path
from .Preset import Preset


class Bootstrap(Preset):
    """
    Configure the front-end scaffolding for the application to use Bootstrap
    """

    key = "bootstrap"
    packages = {
        "bootstrap": "^5.1.3",
        "resolve-url-loader": "^4.0.0",
        "sass": "^1.45.1",
        "sass-loader": "^12.4.0",
    }

    def install(self):
        """Install the preset"""
        self.update_packages(dev=True)
        self.update_webpack_mix()
        self.update_css()
        self.remove_node_modules()

    def update_css(self):
        """Create/Override an app.scss file configured for the preset."""
        shutil.copyfile(
            self.get_template_path("_variables.scss"),
            resources_path("css/_variables.scss"),
        )
        shutil.copyfile(
            self.get_template_path("app.scss"), resources_path("css/app.scss")
        )

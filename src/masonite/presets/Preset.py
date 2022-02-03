import os
import shutil
import json

from ..utils.location import base_path, resources_path
from ..utils.filesystem import get_module_dir, make_full_directory


class Preset:
    """Base preset class containing business logic for adding a preset to the project."""

    key = ""
    packages = {}
    removed_packages = []

    def get_base_stubs_directory(self):
        return os.path.join(get_module_dir(__file__), "../stubs/presets/base/")

    def get_stubs_directory(self):
        return os.path.join(get_module_dir(__file__), f"../stubs/presets/{self.key}/")

    def get_base_template_path(self, template):
        return os.path.join(self.get_base_stubs_directory(), template)

    def get_template_path(self, template):
        return os.path.join(self.get_stubs_directory(), template)

    def update_webpack_mix(self):
        """Replace webpack.mix.js with the one from preset."""
        shutil.copyfile(
            self.get_template_path("webpack.mix.js"), base_path("webpack.mix.js")
        )

    def update_packages(self, dev=True):
        """Update the "package.json" file."""
        filepath = base_path("package.json")
        if not os.path.exists(filepath):
            return

        configuration_key = "devDependencies" if dev else "dependencies"

        with open(filepath, "r+") as f:
            packages = json.load(f)
            # add new packages
            packages[configuration_key].update(self.packages)
            # remove packages
            for package in self.removed_packages:
                packages[configuration_key].pop(package, None)

            f.seek(0)  # Rewind to beginning of file
            f.truncate()
            f.write(json.dumps(packages, sort_keys=True, indent=4))

    def update_css(self):
        """Create/Override an app.css file configured for the preset."""
        make_full_directory(resources_path("css"))
        shutil.copyfile(
            self.get_base_template_path("app.css"), resources_path("css/app.css")
        )

    def update_js(self):
        """Create/Override an app.js file configured for the preset."""
        make_full_directory(resources_path("js"))
        shutil.copyfile(self.get_template_path("app.js"), resources_path("js/app.js"))
        shutil.copyfile(
            self.get_base_template_path("bootstrap.js"),
            resources_path("js/bootstrap.js"),
        )

    def remove_node_modules(self):
        """Remove the installed Node modules."""
        for filename in ["package-lock.json", "yarn.lock"]:
            if os.path.exists(base_path(filename)):
                os.remove(filename)
        shutil.rmtree(base_path("node_modules"), ignore_errors=True)

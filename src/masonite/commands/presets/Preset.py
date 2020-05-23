import os
import shutil
import json


class Preset:

    def ensure_component_directory_exists(self):
        """Ensure the component directories we need exist."""
        directory = 'resources/js/components'
        if not os.path.exists(os.path.realpath(directory)):
            os.makedirs(os.path.realpath(directory))

    def update_packages(self, dev=True):
        """Update the "package.json" file."""
        if not os.path.exists(os.path.realpath('package.json')):
            return

        configuration_key = 'devDependencies' if dev else 'dependencies'

        packages = {}
        with open(os.path.realpath('package.json'), 'r+') as f:
            packages = json.load(f)
            packages[configuration_key] = self.update_package_array(
                packages[configuration_key] if configuration_key in packages else {}
            )
            f.seek(0)  # Rewind to beginning of file
            f.truncate()
            f.write(
                json.dumps(packages, sort_keys=True, indent=4)
            )

    def remove_node_modules(self):
        """Remove the installed Node modules."""
        for filename in ['package-lock.json', 'yarn.lock']:
            if os.path.exists(os.path.realpath(filename)):
                os.remove(filename)
        shutil.rmtree('node_modules', ignore_errors=True)

    def create_scss_file(self):
        """Create an empty app.scss file"""
        os.makedirs(os.path.realpath('resources/sass'))
        with open(os.path.realpath('resources/sass/app.scss'), 'w') as f:
            f.write('// Add your Sass here')

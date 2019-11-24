import os
import shutil
import json

class Preset:

    def ensureComponentDirectoryExists(self):
        """
        Ensure the component directories we need exist.
        """
        directory = 'resources/js/components'
        if not os.path.exists(os.path.realpath(directory)):
            os.makedirs(os.path.realpath(directory))

    def updatePackages(self, dev = True):
        """
        Update the "package.json" file.
        """
        if not os.path.exists(os.path.realpath('package.json')):
            return

        configurationKey = 'devDependencies' if dev else 'dependencies'

        packages = {}
        with open(os.path.realpath('package.json'), 'r+') as f:
            packages = json.load(f)
            packages[configurationKey] = self.updatePackageArray(
                packages[configurationKey] if configurationKey in packages else {}
            )
            f.seek(0) # Rewind to beginning of file
            f.truncate()
            f.write(
                json.dumps(packages, sort_keys=True, indent=2)
            )

    def removeNodeModules(self):
        """
        Remove the installed Node modules.
        """
        for filename in ['package-lock.json', 'yarn.lock']:
            if (os.path.exists(os.path.realpath(filename))):
                os.remove(filename)
        shutil.rmtree('node_modules', ignore_errors=True)

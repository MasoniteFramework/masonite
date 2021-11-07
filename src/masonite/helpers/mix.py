import json
from os.path import join, exists

from ..configuration import config
from ..utils.location import base_path
from ..exceptions import MixManifestNotFound, MixFileNotFound


class MixHelper:
    def __init__(self, app):
        self.app = app

    def url(self, path, manifest_dir=""):
        if not path.startswith("/"):
            path = "/" + path

        root_url = config("application.mix_base_url") or config("application.app_url")

        # load manifest file
        manifest_file = base_path(join(manifest_dir, "mix-manifest.json"))
        if not exists(manifest_file):
            raise MixManifestNotFound(
                "Mix manifest file mix-manifest.json does not exist."
            )
        manifest = {}
        with open(manifest_file, "r") as f:
            manifest = json.load(f)

        # build asset path
        try:
            compiled_path = manifest[path]
        except KeyError:
            raise MixFileNotFound(f"Can't locate mix file: {path}.")
        return join(root_url, compiled_path.lstrip("/"))

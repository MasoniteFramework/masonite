import pathlib
import json
from tests import TestCase

from src.masonite.helpers import MixHelper
from src.masonite.exceptions import MixFileNotFound, MixManifestNotFound
from src.masonite.facades import Config


class TestMix(TestCase):
    def setUp(self):
        super().setUp()
        self.mix = MixHelper(self.application).url
        self.manifest_file = "mix-manifest.json"

    def tearDown(self):
        super().tearDown()
        try:
            # missing_ok=True is only available starting from Python3.8
            pathlib.Path(self.manifest_file).unlink()
        except FileNotFoundError:
            pass

    def _make_manifest(self):
        manifest = {"/storage/app.css": "/static/app.css"}
        with open("mix-manifest.json", "w") as f:
            json.dump(manifest, f)

    def test_mix_without_manifest_raise_exception(self):
        with self.assertRaises(MixManifestNotFound):
            self.mix("/storage/app.css")

    def test_mix_with_wrong_path_raise_exception(self):
        self._make_manifest()
        with self.assertRaises(MixFileNotFound):
            self.mix("/storage/wrong.css")

    def test_mix_url(self):
        self._make_manifest()
        self.assertEqual(
            self.mix("/storage/app.css"), "http://localhost:8000/static/app.css"
        )
        # also works if missing / prefix
        self.assertEqual(
            self.mix("storage/app.css"), "http://localhost:8000/static/app.css"
        )

    def test_mix_with_mix_base_url(self):
        Config.set("application.mix_base_url", "https://some-cdn.com/")
        self._make_manifest()
        self.assertEqual(
            self.mix("storage/app.css"), "https://some-cdn.com/static/app.css"
        )
        Config.set("application.mix_base_url", None)

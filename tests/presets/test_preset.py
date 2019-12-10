import shutil
import os

from src.masonite.commands.presets.Preset import Preset

import unittest


class TestPreset(unittest.TestCase):

    def test_remove_node_modules(self):
        Preset().remove_node_modules()
        self.assertFalse(os.path.exists('package-lock.json'))
        self.assertFalse(os.path.exists('yarn.lock'))
        self.assertFalse(os.path.exists('node_modules'))

    def test_ensure_component_directory_exists(self):
        Preset().ensure_component_directory_exists()
        self.assertTrue(os.path.exists('resources/js/components'))
        shutil.rmtree('resources/js')

    def test_update_packages(self):
        # Preset().update_packages()
        # TODO: Not sure how to test this just yet
        pass

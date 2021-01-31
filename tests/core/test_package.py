import os
import unittest

from src.masonite.packages import create_controller, create_or_append_config

PACKAGE_DIRECTORY = os.getcwd()


class TestPackageHelpers(unittest.TestCase):
    def test_create_config(self):
        create_or_append_config(
            os.path.join(PACKAGE_DIRECTORY, "testpackage/test-config.py")
        )
        self.assertTrue(os.path.exists("config/test-config.py"))
        os.remove("config/test-config.py")

    def test_append_config(self):
        create_or_append_config(
            os.path.join(PACKAGE_DIRECTORY, "testpackage/test-config.py")
        )
        create_or_append_config(
            os.path.join(PACKAGE_DIRECTORY, "testpackage/test-config.py")
        )
        self.assertTrue(os.path.exists("config/test-config.py"))
        with open(os.path.join(PACKAGE_DIRECTORY, "config/test-config.py")) as f:
            self.assertIn("ROUTES = []", f.read())
        os.remove("config/test-config.py")

    def test_create_controller(self):
        create_controller(os.path.join(PACKAGE_DIRECTORY, "testpackage/test-config.py"))
        self.assertTrue(os.path.exists("app/http/controllers/test-config.py"))
        os.remove("app/http/controllers/test-config.py")

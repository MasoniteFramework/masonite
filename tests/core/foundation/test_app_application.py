from tests import TestCase
from src.masonite.foundation import Application
import os


class TestAppApplication(TestCase):
    def test_initialize_application(self):
        app = Application(os.getcwd())
        self.assertTrue(app)

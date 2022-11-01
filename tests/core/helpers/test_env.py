from tests import TestCase

from src.masonite.helpers import env


class TestConfigHelper(TestCase):
    def test_can_get_environment_variable(self):
        self.assertEqual(env("APP_URL"), "http://localhost:8000")

    def test_env_cast_variable_by_default(self):
        self.assertEqual(env("APP_DEBUG"), True)
        self.assertEqual(env("APP_DEBUG", cast=False), "True")

    def test_env_accepts_default_value(self):
        self.assertEqual(env("SOME_APP_VAR", "Masonite Project"), "Masonite Project")

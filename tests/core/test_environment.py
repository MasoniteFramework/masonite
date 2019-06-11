
from masonite.environment import LoadEnvironment
from masonite import env

import os
import unittest


class TestEnvironment(unittest.TestCase):

    def test_environment_loads_custom_env(self):
        LoadEnvironment('local')
        self.assertIn('LOCAL', os.environ)
        self.assertEqual(os.environ.get('LOCAL'), 'TEST')

    def test_environment_only_loads(self):
        LoadEnvironment(only='local')
        self.assertIn('LOCAL', os.environ)
        self.assertEqual(os.environ.get('LOCAL'), 'TEST')


class TestEnv(unittest.TestCase):

    def test_env_returns_numeric(self):
        os.environ["numeric"] = "1"
        self.assertEqual(env('numeric'), 1)

    def test_env_returns_numeric_with_default(self):
        os.environ["numeric"] = "1"
        self.assertEqual(env('na', '1'), 1)

    def test_env_returns_bool(self):
        os.environ["bool"] = "True"
        self.assertTrue(env('bool'))
        os.environ["bool"] = "true"
        self.assertTrue(env('bool'))
        os.environ["bool"] = "False"
        self.assertFalse(env('bool'))
        os.environ["bool"] = "false"
        self.assertFalse(env('bool'))

    def test_env_returns_default(self):
        os.environ["test"] = "1"
        self.assertEqual(env('na', 'default'), 'default')

    def test_env_returns_false_on_blank_string(self):
        os.environ["test"] = ""
        self.assertEqual(env('test', 'default'), 'default')

    def test_env_returns_casted_value_on_blank_string(self):
        os.environ["test"] = ""
        self.assertEqual(env('test', '1234'), 1234)

    def test_env_works_with_none(self):
        self.assertIsNone(env('na', None))

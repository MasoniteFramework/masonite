import pydoc

from masonite.helpers import config, Dot
from config import database
import unittest


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config = config

    def test_config_can_get_value_from_file(self):
        self.assertEqual(self.config('application.DEBUG'), True)

    def test_config_can_get_dict_value_lowercase(self):
        self.assertEqual(self.config('application.debug'), True)

    def test_config_can_get_dict_default(self):
        self.assertEqual(self.config('sdff.na', 'default'), 'default')

    def test_config_not_found_returns_default(self):
        self.assertEqual(self.config('application.nothere', 'default'), 'default')

    def test_dict_dot_returns_value(self):
        self.assertEqual(Dot().dict_dot('s3.test', {'s3': {'test': 'value'}}, ''), 'value')

    def test_config_can_get_dict_value_inside_dict(self):
        self.assertEqual(self.config('database.DATABASES.default'), database.DATABASES['default'])

    def test_config_can_get_dict_value_inside_dict_with_lowercase(self):
        self.assertEqual(self.config('database.databases.default'), database.DATABASES['default'])

    def test_config_can_get_dict_inside_dict_inside_dict(self):
        self.assertIsInstance(self.config('database.databases.sqlite'), dict)

    def test_config_can_get_dict_inside_dict_inside_another_dict(self):
        self.assertEqual(self.config('storage.DRIVERS.s3.test_locations.test'), 'value')

    def test_dot_dict(self):
        self.assertEqual(Dot().dict_dot('async.driver', {'async': {'driver': 'me'}}, 'you'), 'me')

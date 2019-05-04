
import unittest
from masonite.validation.Validator import Validator, required, numeric, json as vjson, length, string
import json

class TestValidation(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_required(self):
        validate = Validator({
            'test': 1
        }, required(['user', 'email']))

        self.assertEqual(validate.errors, ['user is required', 'email is required'])

        validate = Validator({
            'test': 1
        }, required(['test']))

        self.assertEqual(len(validate.errors), 0)

    def test_numeric(self):
        validate = Validator({
            'test': 1
        }, numeric(['test']))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator({
            'test': 'hey'
        }, numeric(['test']))

        self.assertEqual(validate.errors, ['test must be a numeric'])

    def test_several_tests(self):
        validate = Validator({
            'test': 'hey'
        }, required(['notin']), numeric(['notin']))

        self.assertEqual(validate.errors, ['notin is required'])

    def test_json(self):
        validate = Validator({
            'json': 'hey'
        }, vjson(['json']))

        self.assertEqual(validate.errors, ['json must be json'])

        validate = Validator({
            'json': json.dumps({'test': 'key'})
        }, vjson(['json']))

        self.assertEqual(len(validate.errors), 0)

    def test_length(self):
        validate = Validator({
            'json': 'hey'
        }, length(['json'], min=1, max=10))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator({
            'json': 'this is a really long string'
        }, length(['json'], min=1, max=10))

        self.assertEqual(validate.errors, ['json length must be between 1 and 10'])

    def test_string(self):
        validate = Validator({
            'text': 'hey'
        }, string(['text']))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator({
            'text': 1
        }, string(['text']))

        self.assertEqual(validate.errors, ['text must be a string'])



import json
import unittest

from masonite.validation.Validator import Validator
from masonite.validation.Validator import json as vjson
from masonite.validation.Validator import (length, none, numeric, required,
                                           string, equals, truthy, vrange)


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

    def test_none(self):
        validate = Validator({
            'text': None
        }, none(['text']))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator({
            'text': 1
        }, none(['text']))

        self.assertEqual(validate.errors, ['text must be None'])

    def test_equals(self):
        validate = Validator({
            'text': 'test1'
        }, equals(['text'], 'test1'))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator({
            'text': 'test2'
        }, equals(['text'], 'test1'))

        self.assertEqual(validate.errors, ['text must be equal to test1'])

    def test_truthy(self):
        validate = Validator({
            'text': 'value'
        }, truthy(['text']))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator({
            'text': 1
        }, truthy(['text']))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator({
            'text': False
        }, truthy(['text']))

        self.assertEqual(validate.errors, ['text must be a truthy value'])

    def test_vrange(self):
        validate = Validator({
            'text': 52
        }, vrange(['text'], min=25, max=72))

        self.assertEqual(len(validate.errors), 0)

        validate = Validator({
            'text': 101
        }, vrange(['text'], min=25, max=72))

        self.assertEqual(validate.errors, ['text must be between 25 and 72'])

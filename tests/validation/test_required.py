
import unittest
from masonite.validation.Validator import Validator

class TestRequired(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_required_calls_required(self):
        validate = Validator({
            'test': 1
        }, {
            'user': 'required'
        })

        self.assertEqual(validate.errors['user'], 'The element in required')

        validate = Validator({
            'test': 1,
            'user': 'hey'
        }, {
            'user': 'not_required'
        })

        self.assertNotIn('user', validate.errors)

    def test_numeric_calls_numeric(self):
        validate = Validator({
            'user': 1
        }, {
            'user': 'numeric'
        })

        self.assertNotIn('user', validate.errors)

    def test_several_rules(self):
        validate = Validator({
            'user': 1
        }, {
            'user': 'required|numeric'
        })

        self.assertNotIn('user', validate.errors)

    def test_json_rule(self):
        import json
        validate = Validator({
            'user': json.dumps({'user': 1})
        }, {
            'user': 'required|json'
        })

        self.assertNotIn('user', validate.errors)

        validate = Validator({
            'user': 1
        }, {
            'user': 'required|json'
        })

        self.assertEqual(validate.errors['user'], 'The element needs to be a JSON object')

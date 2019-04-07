import unittest

from validator import Length, Pattern, Required

from masonite.helpers import validate
from masonite.request import Request
from masonite.testsuite.TestSuite import generate_wsgi
from masonite.validator import Validator


class TestValidator(unittest.TestCase):

    def setUp(self):
        self.request = Request(generate_wsgi())
        self.request.request_variables = {'id': '1'}

    def test_validator_sets_request(self):
        validator = Validator(self.request)
        self.assertEqual(validator.request, self.request)

    def test_email_validator_sets_dictionary(self):
        email_validator = Validator(self.request)
        email_validator.validate({'id': 1})
        self.assertEqual(email_validator.validation_dictionary, {'id': 1})

    def test_validator_check_does_not_match(self):
        email_validator = Validator(self.request)
        email_validator.validate({'id': [Required, Pattern('[a-zA-Z]')]})
        assert email_validator.check() is False

    def test_validator_check_matches(self):
        email_validator = Validator(self.request)
        email_validator.validate({'id': [Required, Pattern(r'\d+')]})
        assert email_validator.check() is True

    def test_validator_error(self):
        email_validator = Validator(self.request)
        email_validator.validate({'username': [Required]})
        assert email_validator.check() is False
        self.assertEqual(email_validator.errors()['username'], 'must be present')

    def test_validator_error_without_request(self):
        email_validator = Validator()
        email_validator.validate({'username': [Required]})
        assert email_validator.check({'id': 5}) is False
        self.assertEqual(email_validator.errors()['username'], 'must be present')

    def test_validator_check_matches_without_request(self):
        email_validator = Validator()
        email_validator.validate({'id': [Required, Pattern(r'\d+')]})
        assert email_validator.check({'id': '4'}) is True

    def test_validator_errors_returns_false(self):
        email_validator = Validator()
        email_validator.validate({'id': [Required, Pattern(r'\d+')]})
        assert email_validator.check({'id': '4'}) is True
        assert email_validator.errors() is None

    def test_custom_error_message(self):
        email_validator = Validator()
        email_validator.validate({'id': [Required], 'username': [Required]})
        email_validator.messages(
            {'id': 'change your id', 'username': 'dont forget your username'})

        assert email_validator.check({'tomato': 'true'}) is False
        self.assertEqual(email_validator.errors()['id'], 'change your id')

    def test_custom_error_messages_missing_one(self):
        email_validator = Validator()
        email_validator.validate({'id': [Required]})

        email_validator.messages(
            {'username': 'dont forget your username'})

        assert email_validator.check({'username': '5'}) is False
        self.assertEqual(email_validator.errors()['id'], 'must be present')

    def test_validator_length(self):
        email_validator = Validator()
        email_validator.validate({'id': [Length(0, maximum=2)]})
        assert email_validator.check({'id': [1, 2, 3, 4, 5]}) is False

    def test_validator_length_with_casted_value(self):
        email_validator = CastValidator()
        email_validator.test()
        assert email_validator.check({'id': '1,2'}) is True

    def test_validator_get_with_casted_value(self):
        self.request.request_variables = {'id': '1,2'}
        email_validator = CastValidator(self.request)
        email_validator.test()
        assert email_validator.check()
        self.assertEqual(email_validator.get('id'), ['1', '2'])
        self.assertEqual(self.request.all(), {'id': '1,2'})

    def test_validator_can_get_validation_error(self):
        email_validator = Validator()
        email_validator.validate({'id': [Required]})
        assert email_validator.check({'name': '1,2'}) is False
        self.assertEqual(email_validator.error('id'), 'must be present')
        self.assertEqual(email_validator.error('name'), None)


class TestValidatorHelper(unittest.TestCase):

    def test_helper_validates_data(self):
        self.assertEqual(validate({'id': [Required]}, {'name': '1,2'}), {
            'id': 'must be present'})

        self.assertEqual(validate({'id': [Required]}, {'id': '1,2'}), True)

    def test_helper_validates_with_custom_messages(self):
        self.assertEqual(validate({'id': [Required]}, {'name': '1,2'}, {'id': 'is required'}), {
            'id': 'is required'})


class CastValidator(Validator):

    def test(self):
        return self.validate({
            'id': [Length(0, maximum=2)]
        })

    def cast_id(self, id):
        return id.split(',')

from masonite.request import Request
from masonite.validator import Validator
from validator import Pattern, Required, validate, Length
from masonite.testsuite.TestSuite import generate_wsgi


class TestValidator:

    def setup_method(self):
        wsgi_request = generate_wsgi()
        wsgi_request['QUERY_STRING'] = 'id=1'

        self.request = Request(wsgi_request)

    def test_validator_sets_request(self):
        validator = Validator(self.request)
        assert validator.request is self.request


    def test_email_validator_sets_dictionary(self):
        email_validator = Validator(self.request)
        email_validator.validate({'id': 1})
        assert email_validator.validation_dictionary == {'id': 1}


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
        assert email_validator.errors()['username'] == 'must be present'


    def test_validator_error_without_request(self):
        email_validator = Validator()
        email_validator.validate({'username': [Required]})
        assert email_validator.check({'id': 5}) is False
        assert email_validator.errors()['username'] == 'must be present'


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
        email_validator.messages({'id': 'change your id', 'username': 'dont forget your username'})

        assert email_validator.check({'tomato': 'true'}) is False
        assert email_validator.errors()['id'] == 'change your id'
        assert email_validator.errors()['username'] == 'dont forget your username'


    def test_custom_error_messages_missing_one(self):
        email_validator = Validator()
        email_validator.validate({'id': [Required]})

        email_validator.messages(
            {'username': 'dont forget your username'})

        assert email_validator.check({'username': '5'}) is False
        assert email_validator.errors()['id'] == 'must be present'


    def test_validator_length(self):
        email_validator = Validator()
        email_validator.validate({'id': [Length(0, maximum=2)]})
        assert email_validator.check({'id': [1,2,3,4,5]}) is False

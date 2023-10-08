from tests import TestCase
from src.masonite.validation import Validator

class TestValidation(TestCase):
    def test_can_validate_request(self):
        request = self.make_request(query_string="email=joe@masoniteproject.com")
        validation = request.validate(
            {
                "email": "required",
            }
        )

        self.assertEqual(validation.all(), {})

    def test_can_validate_request_with_no_inputs(self):
        request = self.make_request(query_string="")
        validation = request.validate(
            {
                "email": "required",
            }
        )

        self.assertEqual(validation.all(), {"email": ["The email field is required."]})

    def test_can_forward_validation_calls(self):
        request = self.make_request(query_string="")
        validate = Validator()

        errors = request.validate(
            validate.required(['user', 'email']),
            validate.accepted('terms')
        )

        self.assertIn("The user field is required.", errors.get("user"))
        self.assertIn("The email field is required.", errors.get("email"))
        self.assertIn("The terms must be accepted.", errors.get("terms"))

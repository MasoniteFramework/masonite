from tests import TestCase
from masonite.validation import email, isnt, is_in, numeric
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

    def test_custom_messages(self):
        request = self.make_request(post_data={"not_email": "joe@masonite.com", "age": 20})
        # validator = Validator()
        validate = request.validate(
            isnt(is_in("age", [20, 21]), numeric("age")),
            isnt(email("not_email")),
            {
                "username": "required",
                "valid_email": "required|email",
                "secondary_email": "required|email",
            },
            messages={
                "username.required": "Custom Message for required Username.",
                "not_email.isnt_email": "Custom Message for Email not being an email.",
                "valid_email.required": "Custom Message for required Email.",
                "valid_email.email": "Custom Message for Email being a valid email.",
                "age.isnt_is_in.isnt_numeric": "Custom: Age must not be in 20, 21 and must not be numeric.",
            },
        )

        self.assertIn(
            "Custom: Age must not be in 20, 21 and must not be numeric.",
            validate.get("age"),
        )
        self.assertIn(
            "Custom Message for required Email.",
            validate.get("valid_email"),
        )
        self.assertIn(
            "Custom Message for Email being a valid email.",
            validate.get("valid_email"),
        )
        self.assertIn(
            "Custom Message for Email not being an email.",
            validate.get("not_email"),
        )
        self.assertIn(
            "Custom Message for required Username.",
            validate.get("username"),
        )
        self.assertIn(
            "The secondary_email field is required.",
            validate.get("secondary_email"),
        )
        self.assertIn(
            "The secondary_email must be a valid email address.",
            validate.get("secondary_email"),
        )

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


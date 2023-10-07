from tests import TestCase


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
        request = self.make_request(query_string="")
        validate = request.validate(
            {
                "email": "required|email",
                "username": "required",
                "secondary_email": "required|email"
            },
            messages={
                "email.required": "Custom Message for required Email.",
                "email.email": "Custom Message for Email not being an email.",
                "username.required": "Custom Message for required Username."
            },
        )

        self.assertIn(
            "Custom Message for required Email.",
            validate.get("email"),
        )
        self.assertIn(
            "Custom Message for Email not being an email.",
            validate.get("email"),
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

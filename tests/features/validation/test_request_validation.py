from tests import TestCase


class TestValidation(TestCase):
    def test_can_validate_valid_data_request(self):
        request = self.make_request(
            query_string="email=joe@masoniteproject.com"
        )
        validation = request.validate(
            {
                "email": "required",
            }
        )

        self.assertEqual(validation.all(), {})

    def test_can_validate_invalid_data_request(self):
        request = self.make_request(query_string="")
        validation = request.validate(
            {
                "email": "required",
            }
        )

        self.assertEqual(validation.all(), {"email": ["The email field is required."]})

    def test_can_customise_validator(self):
        request = self.make_request(
            query_string="password=abcd!POIY-1234"
        )
        validation = request.validate([
            ("password", "strong", {"uppercase":4, "numbers":4, "length":14}),
        ])

        self.assertEqual(validation.all(), {})

    def test_can_multi_validators(self):
        request = self.make_request(
            query_string="first_name=Bob&last_name=Jones&email=joe@masoniteproject.com"
        )
        validation = request.validate([
            (["first_name", "last_name", "email"], "required"),
            ("email", "email"),
        ])

        self.assertEqual(validation.all(), {})

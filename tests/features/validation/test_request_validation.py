from tests import TestCase


class TestValidation(TestCase):
    def test_can_validate_request(self):
        request = self.make_request(
            data={"QUERY_STRING": "email=joe@masoniteproject.com"}
        )
        validation = request.validate(
            {
                "email": "required",
            }
        )

        self.assertEqual(validation.all(), {})

    def test_can_validate_request(self):
        request = self.make_request(query_string="")
        validation = request.validate(
            {
                "email": "required",
            }
        )

        self.assertEqual(validation.all(), {"email": ["The email field is required."]})

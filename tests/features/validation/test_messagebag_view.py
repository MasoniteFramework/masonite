import unittest
from src.masonite.validation import MessageBag


class TestMessageBag(unittest.TestCase):
    def setUp(self):
        self.errors = MessageBag.view_helper(
            {"email": ["email is required", "email must be a valid email"]}
        )

    def test_get_errors(self):
        self.assertTrue(self.errors.any())

    def test_get_messages(self):
        self.assertIn("email is required", self.errors.messages())
        self.assertIn("email must be a valid email", self.errors.messages())

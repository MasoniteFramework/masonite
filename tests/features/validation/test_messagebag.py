import unittest
from src.masonite.validation import MessageBag


class TestMessageBag(unittest.TestCase):
    def setUp(self):
        self.bag = MessageBag()

    def test_message_bag_can_add_errors_and_messages(self):
        self.bag.add("email", "Your email is invalid")
        self.assertEqual(self.bag.items, {"email": ["Your email is invalid"]})

    def test_message_bag_can_add_several_errors_and_messages(self):
        self.bag.add("email", "Your email is invalid")
        self.bag.add("email", "Your email is invalid")

    def test_message_bag_can_get_all_errors_and_messages(self):
        self.bag.reset()
        self.bag.add("email", "Your email is invalid")
        self.assertEqual(self.bag.all(), {"email": ["Your email is invalid"]})

    def test_message_bag_has_any_errors(self):
        self.bag.reset()
        self.assertFalse(self.bag.any())
        self.bag.add("email", "Your email is invalid")
        self.assertTrue(self.bag.any())

    def test_message_bag_has_any_errors(self):
        self.bag.reset()
        self.assertTrue(self.bag.empty())
        self.bag.add("email", "Your email is invalid")
        self.assertFalse(self.bag.empty())

    def test_message_bag_can_get_first_error(self):
        self.bag.reset()
        self.bag.add("email", "Your email is invalid")
        self.bag.add("email", "Your email is too short")
        self.bag.add("username", "Your username is invalid")
        self.assertEqual(self.bag.first("email"), "Your email is invalid")
        self.assertEqual(self.bag.first("username"), "Your username is invalid")

    def test_amount_of_messages(self):
        self.bag.reset()
        self.bag.add("email", "Your email is invalid")
        self.bag.add("email", "Your email too short")
        self.assertEqual(self.bag.amount("email"), 2)

    def test_has_message(self):
        self.bag.reset()
        self.assertFalse(self.bag.has("email"))
        self.assertFalse(self.bag.has("username"))
        self.bag.add("email", "Your email is invalid")
        self.bag.add("email", "Your email too short")
        self.assertTrue(self.bag.has("email"))
        self.assertFalse(self.bag.has("username"))

    def test_get_messages_with_same_keys(self):
        self.bag.reset()
        self.bag.add("email", "Your email is invalid")
        self.bag.add("email", "Your email too short")
        self.assertIn(
            "Your email is invalid",
            self.bag.get("email"),
        )
        self.assertIn(
            "Your email too short",
            self.bag.get("email"),
        )

    def test_get_errors(self):
        self.bag.reset()
        self.bag.add("email", "Your email is invalid")
        self.bag.add("email", "Your email too short")
        self.assertEqual(self.bag.errors(), ["email"])

    def test_get_messages(self):
        self.bag.reset()
        self.bag.add("email", "Your email is invalid")
        self.bag.add("username", "Your username too short")
        self.assertIn(
            "Your email is invalid",
            self.bag.messages(),
        )

        self.assertIn(
            "Your username too short",
            self.bag.messages(),
        )

    def test_can_convert_to_json(self):
        self.bag.reset()
        self.bag.add("email", "Your email is invalid")
        self.assertEqual(self.bag.json(), '{"email": ["Your email is invalid"]}')

    def test_can_merge(self):
        self.bag.reset()
        self.bag.add("email", "Your email is invalid")
        self.bag.merge({"username": ["username is too short"]})
        self.assertEqual(self.bag.count(), 2)

    def test_can_work_with_if_statements_and_full(self):
        self.bag.reset()
        self.bag.add("email", "Your email is invalid")

        if self.bag:
            pass
        else:
            raise AssertionError("Should assert true as a boolean")

    def test_can_work_with_if_statements_and_false(self):
        self.bag.reset()

        if self.bag:
            raise AssertionError("Should not raise when not full")
        else:
            pass

from tests import TestCase

from src.masonite.utils.str import random_string, removeprefix, removesuffix


class TestStringsUtils(TestCase):
    def test_random_string(self):
        self.assertEqual(len(random_string()), 4)
        self.assertEqual(len(random_string(10)), 10)
        self.assertIsInstance(random_string(5), str)
        self.assertNotEqual(random_string(), random_string())

    def test_removesuffix(self):
        self.assertEqual(removesuffix("test.com", ".com"), "test")
        self.assertEqual(removesuffix("test", ".com"), "test")

    def test_removeprefix(self):
        self.assertEqual(removeprefix("AppEvent", "App"), "Event")
        self.assertEqual(removeprefix("Event", "App"), "Event")

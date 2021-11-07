from tests import TestCase

from src.masonite.helpers import optional


class SomeClass:

    my_attr = 3

    def my_method(self):
        return 4


class TestOptionalHelper(TestCase):
    def test_optional_with_existing(self):
        obj = SomeClass()
        self.assertEqual(optional(obj).my_attr, 3)
        self.assertEqual(optional(obj).my_method(), 4)

    def test_optional_with_undefined(self):
        obj = SomeClass()
        self.assertEqual(optional(obj).non_existing_attr, None)
        self.assertEqual(optional(obj).non_existing_method(), None)

    def test_optional_with_default(self):
        obj = SomeClass()
        self.assertEqual(optional(obj, default=0).non_existing_attr, 0)
        self.assertEqual(optional(obj, default=0).non_existing_method(), 0)

from tests import TestCase

from src.masonite.helpers import optional


class SomeClass:

    my_attr = 3

    def my_method(self):
        return 4


class TestOptionalHelper(TestCase):
    def test_optional_with_existing(self):
        obj = SomeClass()
        assert optional(obj).my_attr == 3
        assert optional(obj).my_method() == 4

    def test_optional_with_undefined(self):
        obj = SomeClass()
        assert optional(obj).non_existing_attr is None

        # not beautiful but we can do this to handle calling methods
        assert optional(optional(obj).non_existing_method)() is None

    def test_optional_with_undefined_on_none(self):
        obj = None
        assert optional(obj).non_existing_attr is None

    def test_optional_with_default(self):
        obj = SomeClass()
        assert optional(obj, 0).non_existing_attr == 0

    def test_optional_with_callable_default(self):
        obj = SomeClass()
        assert optional(obj, lambda the_obj: "a").non_existing_attr == "a"

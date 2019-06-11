from masonite.helpers import optional
import unittest

class MockUser:
    id = 1

class CallThis:

    def method(self, var):
        self.test = var
        return self

class TestOptional(unittest.TestCase):

    def test_optional_returns_object_id(self):
        self.assertEqual(optional(MockUser).id, 1)
        self.assertTrue(optional(object).id) # It's a class
        self.assertTrue(optional(None).id) # It's a class
        self.assertEqual(optional(object).instance(), object)
    
    def test_optional_can_handle_method_calls(self):
        self.assertFalse(optional(MockUser).method())
        self.assertEqual(optional(CallThis()).method('test').test, 'test')

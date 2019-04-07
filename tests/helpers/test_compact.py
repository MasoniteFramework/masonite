from masonite.helpers import compact
from masonite.request import Request
from masonite.exceptions import AmbiguousError

import unittest

class TestCompact(unittest.TestCase):

    def test_compact_returns_dict_of_local_variable(self):
        x = 'hello'
        self.assertEqual(compact(x), {'x': 'hello'})
    
    def test_works_with_several_variables(self):
        x = 'hello'
        y = 'world'
        self.assertEqual(compact(x, y), {'x': 'hello', 'y': 'world'})
    
    def test_can_contain_dict(self):
        x = 'hello'
        y = 'world'
        self.assertEqual(compact(x, y, {'z': 'foo'}), {'x': 'hello', 'y': 'world', 'z': 'foo'})

    def test_exception_on_too_many(self):
        x = 'hello'
        y = 'world'
        with self.assertRaises(ValueError):
            compact(x, y, 'z')

    def test_compact_throws_exceptions(self):
        r = Request(None)
        request = r
        with self.assertRaises(AmbiguousError):
            compact(request)

    def test_works_with_classes(self):
        request = Request(None)
        self.assertIn('request', compact(request))

import pytest
from masonite.helpers import dot, Dot as DictDot
import unittest

class TestDot(unittest.TestCase):

    def test_dot(self):
        self.assertEqual(dot('hey.dot', compile_to="{1}[{.}]"), "hey[dot]")
        self.assertEqual(dot('hey.dot.another', compile_to="{1}[{.}]"), "hey[dot][another]")
        self.assertEqual(dot('hey.dot.another.and.another', compile_to="{1}[{.}]"), "hey[dot][another][and][another]")
        self.assertEqual(dot('hey.dot.another.and.another', compile_to="/{1}[{.}]"), "/hey[dot][another][and][another]")
        self.assertEqual(dot('hey.dot', compile_to="{1}/{.}"), "hey/dot")
        self.assertEqual(dot('hey.dot.another', compile_to="{1}/{.}"), "hey/dot/another")
        self.assertEqual(dot('hey.dot.another', compile_to="{1}/{.}"), "hey/dot/another")
        self.assertEqual(dot('hey.dot.another', compile_to="/{1}/{.}"), "/hey/dot/another")
        with pytest.raises(ValueError):
            self.assertEqual(dot('hey.dot.another', compile_to="{1}//{.}"), "hey/dot/another")

    def test_dict_dot(self):
        self.assertEqual(DictDot().dot('key', {'key': 'value'}), 'value')
        self.assertEqual(DictDot().dot('key.test', {'key': {'test': 'value'}}), 'value')
        self.assertEqual(DictDot().dot('key.test.layer', {'key': {'test': {'layer': 'value'}}}), 'value')
        self.assertEqual(DictDot().dot('key.none', {'key': {'test': {'layer': 'value'}}}), None)
        self.assertEqual(DictDot().dot('key', {'key': {'test': {'layer': 'value'}}}), {'test': {'layer': 'value'}})

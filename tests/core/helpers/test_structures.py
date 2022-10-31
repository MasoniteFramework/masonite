from tests import TestCase

from src.masonite.helpers import collect, flatten
from src.masonite.utils.collections import Collection


class TestStructuresHelper(TestCase):
    def test_can_collect_iterables(self):
        iterable = [1, 2, 3]
        self.assertIsInstance(collect(iterable), Collection)
        self.assertEqual(collect(iterable).first(), 1)

        iterable = {"id": 1, "id": 2}
        self.assertIsInstance(collect(iterable), Collection)

    def test_can_flatten_iterables(self):
        iterable = [1, ["a", ["1.", "2."]], 2, 3]
        self.assertEqual(flatten(iterable), [1, "a", "1.", "2.", 2, 3])

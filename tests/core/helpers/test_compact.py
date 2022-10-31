from unittest import TestCase
from src.masonite.helpers import compact


class TestCompactHelper(TestCase):
    def test_compact(self):
        users = [1, 2]
        comments = ["foo", "bar"]
        data = compact(users, comments)
        self.assertDictEqual(data, {"users": users, "comments": comments})

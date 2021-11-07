import unittest
from src.masonite.headers import HeaderBag, Header


class TestHeaders(unittest.TestCase):
    def test_headers_can_be_registered(self):
        bag = HeaderBag()
        bag.add(Header("Content-Type", "application/json"))
        self.assertTrue(bag["CONTENT_TYPE"])

    def test_headers_can_be_rendered(self):
        bag = HeaderBag()
        bag.add(Header("content-type", "application/json"))
        bag.add(Header("x-forwarded-for", "127.0.0.1"))
        self.assertEqual(
            bag.render(),
            [("Content-Type", "application/json"), ("X-Forwarded-For", "127.0.0.1")],
        )

    def test_headers_can_check_with_in(self):
        bag = HeaderBag()
        bag.add(Header("Content-Type", "application/json"))

        self.assertTrue("Content-Type" in bag)

    def test_headers_can_be_retrieved(self):
        bag = HeaderBag()
        bag.add(Header("Content-Type", "application/json"))
        self.assertEqual(bag.get("content-type").value, "application/json")
        self.assertEqual(bag.get("Content-Type").value, "application/json")

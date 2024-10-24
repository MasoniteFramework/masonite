from tests import TestCase

from src.masonite.response import Response


class TestResponse(TestCase):
    def test_with_headers(self):
        response = Response(self.application)
        response = response.with_headers({"X-Test": "value", "X-Rate-Limited": "true"})
        self.assertIsInstance(response, Response)
        self.assertEqual(response.header("X-Test"), "value")
        self.assertEqual(response.header("X-Rate-Limited"), "true")

    def test_encoding_chinese_characters(self):
        response = Response(self.application)
        content = response.json({"test": "我"})
        self.assertEqual(content.decode("utf-8"), '{"test": "我"}')

    def test_redirect_external(self):
        response = Response(self.application)
        response = response.redirect("https://google.com")
        self.assertEqual(response._status, "302 Found")
        self.assertEqual(response.header_bag.get("Location").value, "https://google.com")

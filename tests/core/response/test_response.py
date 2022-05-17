from tests import TestCase

from src.masonite.response import Response


class TestResponse(TestCase):
    def test_with_headers(self):
        response = Response(self.application)
        response = response.with_headers({"X-Test": "value", "X-Rate-Limited": "true"})
        self.assertIsInstance(response, Response)
        self.assertEqual(response.header("X-Test"), "value")
        self.assertEqual(response.header("X-Rate-Limited"), "true")

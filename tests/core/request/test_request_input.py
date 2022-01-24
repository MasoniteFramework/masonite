from tests import TestCase

from src.masonite.utils.http import generate_wsgi
from src.masonite.request import Request


class TestRequest(TestCase):
    def setUp(self):
        super().setUp()
        self.request = Request(generate_wsgi(path="/test"))

    def test_request_no_input_returns_empty_string(self):
        self.assertEqual(self.request.input("notavailable"), "")

    def test_request_can_get_string_value(self):
        self.request.input_bag.query_string = {"test": "value"}
        self.assertEqual(self.request.input("test"), "value")

    def test_request_can_get_list_value(self):
        self.request.input_bag.query_string = {"test": ["foo", "bar"]}
        self.assertEqual(self.request.input("test"), ["foo", "bar"])

    def test_request_can_get_float_value(self):
        self.request.input_bag.query_string = {"test": 3.1415926}
        self.assertEqual(self.request.input("test"), 3.1415926)

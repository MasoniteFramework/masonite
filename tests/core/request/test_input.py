import binascii
import os
import json
import io

from src.masonite.input import InputBag
from src.masonite.tests import MockInput
from tests import TestCase


def encode_multipart_formdata(fields):
    boundary = binascii.hexlify(os.urandom(16)).decode("ascii")

    body = (
        "".join(
            "--%s\r\n"
            'Content-Disposition: form-data; name="%s"\r\n'
            "\r\n"
            "%s\r\n" % (boundary, field, value)
            for field, value in fields.items()
        )
        + "--%s--\r\n" % boundary
    )

    content_type = "multipart/form-data; boundary=%s" % boundary

    return body, content_type


class TestInput(TestCase):
    def setUp(self):
        super().setUp()
        self.post_data = MockInput(
            '{"param": "hey", "foo": [9, 8, 7, 6], "bar": "baz"}'
        )
        self.bytes_data = MockInput(b"jack=Daniels")

    def test_can_parse_query_string(self):
        bag = InputBag()
        bag.load({"QUERY_STRING": "hello=you&goodbye=me"})
        self.assertEqual(bag.get("hello"), "you")
        self.assertEqual(bag.get("goodbye"), "me")

    def test_can_parse_post_data(self):
        bag = InputBag()
        bag.load(
            {
                "CONTENT_LENGTH": len(str(json.dumps({"__token": 1}))),
                "wsgi.input": io.BytesIO(bytes(json.dumps({"__token": 1}), "utf-8")),
            }
        )
        self.assertEqual(bag.get("__token"), 1)

    def test_can_parse_duplicate_values(self):
        bag = InputBag()
        bag.load({"QUERY_STRING": "filter[name]=Joe&filter[last]=Bill"})
        """
            {"filter": [{}]}
        """
        self.assertTrue("name" in bag.get("filter"))
        self.assertTrue("last" in bag.get("filter"))

    def test_all_with_values(self):
        bag = InputBag()
        bag.load({"QUERY_STRING": "hello=you"})
        """
            {"filter": [{}]}
        """
        self.assertEqual(bag.all_as_values(), {"hello": "you"})

    def test_can_get_defaults(self):
        bag = InputBag()
        bag.load({"QUERY_STRING": ""})
        self.assertEqual(bag.get("hello", "default"), "default")
        self.assertEqual(
            bag.get("hello"), None
        )  # TODO: This should probably return a blank string instead of None
        self.assertEqual(bag.get("hello[]"), [])

    def test_all_without_internal_values(self):
        bag = InputBag()
        bag.load({"QUERY_STRING": "hello=you&__token=tok"})
        """
            {"filter": [{}]}
        """
        self.assertEqual(bag.all_as_values(internal_variables=False), {"hello": "you"})

    def test_has(self):
        bag = InputBag()
        bag.load({"QUERY_STRING": "hello=you&goodbye=me"})
        self.assertTrue(bag.has("hello", "goodbye"))

    def test_only(self):
        bag = InputBag()
        bag.load({"QUERY_STRING": "hello=you&goodbye=me&name=Joe"})
        self.assertEqual(bag.only("hello", "name"), {"hello": "you", "name": "Joe"})

    def test_only_array_based_inputs(self):
        bag = InputBag()
        bag.load({"QUERY_STRING": "user[]=user1&user[]=user2"})
        self.assertEqual(bag.get("user[]"), ["user1", "user2"])
        bag = InputBag()
        bag.load({"QUERY_STRING": "user[user1]=value&user[user2]=value"})
        self.assertEqual(bag.get("user"), {"user1": "value", "user2": "value"})

    def test_can_parse_text_plain_content_type(self):
        post_data = MockInput(
            '{"param": "hey", "foo": [9, 8, 7, 6], "bar": "baz"}'.encode("utf-8")
        )
        bag = InputBag()
        bag.load({"wsgi.input": post_data, "CONTENT_TYPE": "text/plain"})
        self.assertEqual(bag.get("param"), "hey")

    def test_can_parse_application_json_content_type(self):
        bag = InputBag()
        bag.load({"wsgi.input": self.post_data, "CONTENT_TYPE": "application/json"})
        self.assertEqual(bag.get("param"), "hey")

    def test_can_parse_form_urlencoded_content_type(self):
        bag = InputBag()
        bag.load(
            {
                "wsgi.input": self.bytes_data,
                "CONTENT_TYPE": "application/x-www-form-urlencoded",
            }
        )
        self.assertEqual(bag.get("jack"), "Daniels")

    def test_can_parse_multipart_formdata_content_type(self):
        data, content_type = encode_multipart_formdata({"key": "value", "test": 1})
        bag = InputBag()
        bag.load(
            {
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": content_type,
                "CONTENT_LENGTH": str(len(data.encode("utf-8"))),
                "wsgi.input": io.BytesIO(data.encode("utf-8")),
            }
        )

        self.assertEqual(bag.get("key"), "value")
        self.assertEqual(bag.get("test"), "1")

    def test_advanced_dict_parse(self):
        bag = InputBag()
        inputs = bag.parse_dict(
            {"user[][name]": ["Joe"], "user[][email]": ["joe@masoniteproject.com"]}
        )
        self.assertEqual(
            inputs, {"user": [{"name": "Joe"}, {"email": "joe@masoniteproject.com"}]}
        )
        inputs = bag.parse_dict(
            {"user[name]": ["Joe"], "user[email]": ["joe@masoniteproject.com"]}
        )
        self.assertEqual(
            inputs, {"user": {"email": "joe@masoniteproject.com", "name": "Joe"}}
        )

    def test_can_parse_nested_post_data(self):
        # application/json
        bag = InputBag()
        data = {"key": "val", "a": {"b": {"c": 1}}}
        bag.load(
            {
                "CONTENT_TYPE": "application/json",
                "CONTENT_LENGTH": len(str(json.dumps(data))),
                "wsgi.input": io.BytesIO(bytes(json.dumps(data), "utf-8")),
            }
        )
        self.assertEqual(bag.get("key"), "val")
        self.assertEqual(bag.get("a.b.c"), 1)

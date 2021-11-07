from src.masonite.input import InputBag
from src.masonite.tests import MockInput
from tests import TestCase
import json, io


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

    def test_can_parse_post_params(self):
        bag = InputBag()
        bag.load({"wsgi.input": self.post_data, "CONTENT_TYPE": "application/json"})
        self.assertEqual(bag.get("param"), "hey")

    def test_can_parse_post_params_from_url_encoded(self):
        bag = InputBag()
        bag.load(
            {
                "wsgi.input": self.bytes_data,
                "CONTENT_TYPE": "application/x-www-form-urlencoded",
            }
        )
        self.assertEqual(bag.get("jack"), "Daniels")

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
        # inputs = bag.parse_dict({'user[options][name]': ['Joe'], 'user[options][email]': ['joe@masoniteproject.com']})
        # self.assertEqual(inputs, {'user': {"options": {'email': 'joe@masoniteproject.com', 'name': 'Joe'}}}

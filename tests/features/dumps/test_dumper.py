from tests import TestCase

from src.masonite.facades import Dump
from src.masonite.exceptions import DumpException


class TestDumper(TestCase):
    def setUp(self):
        super().setUp()
        self.dumper = self.application.make("dumper")

    def tearDown(self):
        super().tearDown()
        self.dumper.clear()

    def test_get_dumps(self):
        dumps = self.dumper.get_dumps()
        assert dumps == []

    def test_get_serialized_dumps(self):
        dumps = self.dumper.get_serialized_dumps()
        assert dumps == []

    def test_dump(self):
        self.dumper.dump(1, {"test": "value"})
        dumps = self.dumper.get_dumps()
        assert len(dumps) == 1

        first_dump = self.dumper.last()
        assert first_dump.line == 25
        assert first_dump.filename.endswith("test_dumper.py")
        assert first_dump.method == "test_dump"
        assert len(first_dump.objects.keys()) == 2
        assert first_dump.objects.get("<class 'int'>") == 1
        assert first_dump.objects.get("<class 'dict'>") == {"test": "value"}

    def test_dump_can_get_variables_name(self):
        test = 1
        other_test = "a"
        self.dumper.dump(test, other_test)
        test_dump = self.dumper.last()
        assert test_dump.objects.get("test") == 1
        assert test_dump.objects.get("other_test") == "a"

    def test_serialize_dump(self):
        self.dumper.dump(1, {"test": "value"})
        data = self.dumper.last().serialize()
        assert data.get("line") == 46
        assert data.get("filename")
        assert data.get("timestamp")
        assert data.get("method")
        first_object = data.get("objects").get("<class 'int'>")
        assert first_object.get("value") == "1"

    def test_serialize_dump_properties(self):
        class TestObject:
            key = "value"
            _other_key = 1

        my_obj = TestObject()
        self.dumper.dump(my_obj)
        data = self.dumper.last().serialize()
        assert "my_obj" in data.get("objects")
        obj_props = data.get("objects").get("my_obj").get("properties")
        assert obj_props.get("private").get("_other_key") == "1"
        assert obj_props.get("public").get("key") == "value"

    def test_can_add_several_dumps(self):
        self.dumper.dump(1)
        self.dumper.dump(2)
        self.dumper.dump(3)
        assert len(self.dumper.get_dumps()) == 3

    def test_can_clear_dumps(self):
        self.dumper.dump(1)
        self.dumper.dump(2)
        self.dumper.clear()
        assert len(self.dumper.get_dumps()) == 0

    def test_dump_and_die(self):
        self.dumper.dump(1)
        with self.assertRaises(DumpException):
            self.dumper.dd(2)
        assert len(self.dumper.get_dumps()) == 2

    def test_dumps_are_ordered_by_most_recent(self):
        var = 1
        var_latest = 2
        self.dumper.dump(var)
        self.dumper.dump(var_latest)
        assert self.dumper.last().objects.get("var_latest") == 2
        assert self.dumper.get_dumps()[0].objects.get("var_latest") == 2

    def test_can_revert_dump_order(self):
        var = 1
        var_latest = 2
        self.dumper.dump(var)
        self.dumper.dump(var_latest)
        assert self.dumper.get_dumps(ascending=True)[0].objects.get("var") == 1

    def test_dump_facade(self):
        var = "test"
        Dump.dump(var)
        assert Dump.last().objects.get("var") == "test"

    def test_dump_builtins(self):
        var = "test"
        dump(var)
        assert self.dumper.last().objects.get("var") == "test"

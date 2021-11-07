from tests import TestCase

from src.masonite.utils.structures import data_get, data_set, data


class TestStructures(TestCase):
    def test_data_get(self):
        struct = {"key": "val", "a": {"b": "c", "nested": {"a": 1}}}
        self.assertEqual(data_get(struct, "key"), "val")

        self.assertEqual(data_get(struct, "a.b"), "c")
        self.assertEqual(data_get(struct, "a.nested.a"), 1)

        self.assertEqual(data_get(struct, "a.nested.unknown"), None)
        self.assertEqual(data_get(struct, "a.nested.unknown", 0), 0)

    def test_data_set(self):
        struct = {"key": "val", "a": {"b": "c", "nested": {"a": 1}}}
        data_set(struct, "key", "val2")
        self.assertEqual(struct.get("key"), "val2")

        data_set(struct, "a.nested.a", 3)
        self.assertEqual(data_get(struct, "a.nested.a"), 3)

        data_set(struct, "a.unknown", "new")
        self.assertEqual(data_get(struct, "a.unknown"), "new")

    def test_data_set_no_overwrite(self):
        struct = {"key": "val", "a": {"b": "c", "nested": {"a": 1}}}
        data_set(struct, "key", "val2", overwrite=False)
        self.assertEqual(data_get(struct, "key"), "val")

        data_set(struct, "a.nested.a", "new", overwrite=False)
        self.assertEqual(data_get(struct, "a.nested.a"), 1)

        data_set(struct, "unknown.key", "new", overwrite=False)
        self.assertEqual(data_get(struct, "unknown.key"), "new")

    def test_data(self):
        struct = {"key": "val"}
        dotted_struct = data(struct)
        dotted_struct["new_key.nested"] = 3
        self.assertEqual(dotted_struct.get("new_key.nested"), 3)
        self.assertEqual(dotted_struct, {"key": "val", "new_key": {"nested": 3}})

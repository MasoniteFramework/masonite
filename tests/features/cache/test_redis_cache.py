from tests import TestCase
import os
import time
import pytest


@pytest.mark.integrations
class TestRedisCache(TestCase):
    def setUp(self):
        super().setUp()
        self.application.make("cache")
        self.driver = self.application.make("cache").store("redis")

    def test_can_add_file_driver(self):
        self.assertEqual(self.driver.add("add_key", "value"), "value")

    def test_can_get_driver(self):
        self.driver.put("key", "value")
        self.assertEqual(self.driver.get("key"), "value")
        self.assertTrue(self.driver.has("key"), "value")

    def test_can_increment(self):
        self.driver.put("count", "1")
        self.assertEqual(self.driver.get("count"), "1")
        self.driver.increment("count")
        self.assertEqual(self.driver.get("count"), "2")
        self.driver.decrement("count")
        self.assertEqual(self.driver.get("count"), "1")

    def test_will_not_get_expired(self):
        self.driver.put("expire", "1", 1)

        time.sleep(2)
        self.assertEqual(self.driver.get("expire"), None)

    def test_will_get_not_yet_expired(self):
        self.driver.put("expire", "1", 20)
        self.assertEqual(self.driver.get("expire"), "1")

    def test_forget(self):
        self.driver.put("forget", "1")
        self.assertEqual(self.driver.get("forget"), "1")
        self.driver.forget("forget")
        self.assertEqual(self.driver.get("forget"), None)

    def test_remember(self):
        self.driver.remember("remember", lambda cache: (cache.put("remember", "1", 10)))
        self.assertEqual(self.driver.get("remember"), "1")

    def test_remember_datatypes(self):
        self.driver.remember(
            "dic", lambda cache: (cache.put("dic", {"id": 1, "name": "Joe"}, 10))
        )
        self.assertIsInstance(self.driver.get("dic"), dict)
        self.driver.remember("list", lambda cache: (cache.put("list", [1, 2, 3], 10)))
        self.assertIsInstance(self.driver.get("list"), list)

    def test_flush(self):
        self.driver.remember(
            "dic", lambda cache: (cache.put("dic", {"id": 1, "name": "Joe"}, 10))
        )
        self.driver.flush()
        self.assertIsNone(self.driver.get("dic"))

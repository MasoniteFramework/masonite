from tests import TestCase
import os
import time
from src.masonite.filesystem import File


class TestLocalStorage(TestCase):
    def setUp(self):
        super().setUp()
        self.application.make("storage")
        self.driver = self.application.make("storage").disk()

    def test_can_get_file_driver(self):
        self.driver.put("key.log", "value")
        self.assertEqual(self.driver.get("key.log"), "value")
        self.assertTrue(self.driver.exists("key.log"))

    def test_can_move(self):
        self.driver.move("key.log", "logs/key.log")

    def test_can_stream(self):
        self.driver.put("key.log", "value")
        stream = self.driver.stream("key.log")
        self.assertEqual(stream.name(), "key.log")
        self.assertEqual(stream.extension(), ".log")

    def test_can_delete(self):
        self.driver.put("delete.log", "value")
        self.assertEqual(self.driver.get("delete.log"), "value")
        stream = self.driver.delete("delete.log")
        self.assertEqual(self.driver.get("delete.log"), None)

    def test_can_store(self):
        self.driver.store(File(b"hello.log", "hello-world"))

    def test_can_append_file(self):
        self.driver.append("world.log", "hello")
        self.driver.prepend("world.log", "world")

    def test_can_get_contents_of_directory(self):
        self.driver.get_files()

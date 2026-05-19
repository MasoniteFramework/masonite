from tests import TestCase
import time
import pytest


def redis_available():
    try:
        import redis
        r = redis.Redis(host="127.0.0.1", port=6379, socket_connect_timeout=1)
        r.ping()
        return True
    except Exception:
        return False


@pytest.mark.integrations
@pytest.mark.skipif(not redis_available(), reason="Redis server not available")
class TestRedisSession(TestCase):
    def setUp(self):
        super().setUp()
        self.session = self.application.make("session")
        self.driver = self.session.driver("redis")
        self.session.start("redis")

    def teardown(self):
        self.session.flush()
        self.session.close()
        self.session = None

    def test_can_increment(self):
        self.session.set("count", "1")
        self.assertEqual(self.session.get("count"), "1")
        self.session.increment("count")
        self.assertEqual(self.session.get("count"), "2")
        self.session.decrement("count")
        self.assertEqual(self.session.get("count"), "1")

    def test_delete(self):
        self.session.set("forget", "1")
        self.assertEqual(self.session.get("forget"), "1")
        self.session.delete("forget")
        self.assertEqual(self.session.get("forget"), None)

    def test_set(self):
        self.session.set("remember", "1")
        self.assertEqual(self.session.get("remember"), "1")

    def test_can_flash(self):
        self.session.flash("key", "test")
        self.assertEqual(self.session.get("key"), "test")
        self.assertEqual(self.session.get("key"), None)

    def test_can_pull_session(self):
        self.session.set("key", "test")
        self.assertEqual(self.session.get("key"), "test")
        key = self.session.pull("key")
        self.assertEqual(key, "test")
        self.assertEqual(self.session.get("key"), None)

    def test_flush(self):
        self.session.set("dic", {"id": 1, "name": "Joe"})
        self.session.flush()
        self.assertIsNone(self.session.get("dic"))

from tests import TestCase

from src.masonite.helpers import config


class TestConfigHelper(TestCase):
    def test_can_get_config_value(self):
        self.assertEqual(config("application.app_url"), "http://localhost:8000")

    def test_can_get_nested_config_value(self):
        self.assertEqual(config("application.hashing.argon2.threads"), 2)

    def test_can_provide_default_value(self):
        self.assertEqual(
            config("queue.drivers.redis.host", "redis.server"), "redis.server"
        )

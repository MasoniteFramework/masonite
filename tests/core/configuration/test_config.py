from tests import TestCase
from src.masonite.facades import Config
from src.masonite.configuration import config
from src.masonite.exceptions import InvalidConfigurationSetup


PACKAGE_PARAM = 1
OTHER_PARAM = 3


class TestConfiguration(TestCase):
    def test_config_is_loaded(self):
        self.assertGreater(len(Config._config.keys()), 0)

    def test_base_configuration_files_can_be_accessed(self):
        self.assertIsNotNone("config.application")
        self.assertIsNotNone("config.auth")
        self.assertIsNotNone("config.broadcast")
        self.assertIsNotNone("config.cache")
        self.assertIsNotNone("config.database")
        self.assertIsNotNone("config.filesystem")
        self.assertIsNotNone("config.mail")
        self.assertIsNotNone("config.notification")
        self.assertIsNotNone("config.providers")
        self.assertIsNotNone("config.queue")
        self.assertIsNotNone("config.session")

    def test_config_helper(self):
        self.assertEqual(config("auth.guards.default"), "web")

    def test_config_facade(self):
        self.assertEqual(Config.get("auth.guards.default"), "web")

    def test_config_use_default_if_not_exist(self):
        self.assertEqual(config("some.app"), None)
        self.assertEqual(config("some.app", 0), 0)

    def test_config_set_value(self):
        original_value = config("cache.stores.redis.port")
        Config.set("cache.stores.redis.port", 1000)
        self.assertNotEqual(Config.get("cache.stores.redis.port"), original_value)
        self.assertEqual(Config.get("cache.stores.redis.port"), 1000)
        # reset to original value
        Config.set("cache.stores.redis.port", original_value)

    def test_can_load_non_foundation_config_in_project(self):
        self.assertEqual(config("package.package_param"), "package_value")

    def test_cannot_override_foundation_config(self):
        with self.assertRaises(InvalidConfigurationSetup):
            Config.merge_with("auth", {"key": "val"})

    def test_can_merge_external_config_with_project_config(self):
        # reset test package config for idempotent tests
        Config.set("package", {"package_param": "package_value"})

        package_default_config = {"PACKAGE_PARAM": "default_value", "OTHER_PARAM": 2}
        Config.merge_with("package", package_default_config)
        self.assertEqual(config("package.package_param"), "package_value")
        self.assertEqual(config("package.other_param"), 2)

    def test_can_merge_external_config_using_path(self):
        # reset test package config for idempotent tests
        Config.set("package", {"package_param": "package_value"})

        Config.merge_with("package", "tests/core/configuration/test_config.py")
        self.assertEqual(config("package.package_param"), "package_value")
        self.assertEqual(config("package.other_param"), 3)

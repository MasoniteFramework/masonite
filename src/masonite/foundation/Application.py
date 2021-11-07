import os
import sys
from ..container import Container


class Application(Container):
    def __init__(self, base_path=None):
        self.base_path = base_path
        self.storage_path = None
        self.response_handler = None
        self.providers = []

    def set_response_handler(self, response_handler):
        self.response_handler = response_handler

    def get_response_handler(self):
        return self.response_handler

    def register_providers(self, *providers):
        for provider in providers:
            provider = provider(self)
            provider.register()
        return self

    def use_storage_path(self, path):
        self.storage_path = path

    def get_storage_path(self):
        return self.storage_path

    def add_providers(self, *providers):
        for provider in providers:
            provider = provider(self)
            provider.register()
            self.providers.append(provider)

        return self

    def set_controller_locations(self, location):
        self._controller_locations = location

    def get_controller_locations(self, location):
        return self._controller_locations

    def get_providers(self):
        return self.providers

    def __call__(self, *args, **kwargs):
        return self.response_handler(*args, **kwargs)

    def is_dev(self):
        """Check if app is running in development mode."""
        return os.getenv("APP_ENV") == "development"

    def is_production(self):
        """Check if app is running in production mode."""
        return os.getenv("APP_ENV") == "production"

    def is_running_tests(self):
        """Check if app is running tests."""

        return "pytest" in sys.modules

    def is_running_in_console(self):
        """Check if application is running in console. This is useful to only run some providers
        logic when used in console. We can differenciate if the application is being served or
        if an application command is ran in console."""
        if len(sys.argv) > 1:
            return sys.argv[1] != "serve"
        return True

    def environment(self):
        """Helper to get current environment."""
        if self.is_running_tests():
            return "testing"
        else:
            return os.getenv("APP_ENV")

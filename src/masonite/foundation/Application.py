from __future__ import annotations
import os
import sys
from typing import Callable, List, Tuple, TYPE_CHECKING, Iterator, Type

from ..container import Container
from ..facades import Config
from ..environment import env

if TYPE_CHECKING:
    from ..providers import Provider

ResponseHandler = Callable[[str, List[Tuple]], None]


class Application(Container):
    def __init__(self, base_path: str = None):
        self.base_path: str = base_path
        self.storage_path: str = None
        self.response_handler: ResponseHandler
        self.providers: list = []

    def set_response_handler(self, response_handler: ResponseHandler) -> None:
        self.response_handler = response_handler

    def get_response_handler(self) -> ResponseHandler:
        return self.response_handler

    def register_providers(self, *providers: Type["Provider"]) -> "Application":
        for provider_class in providers:
            provider = provider_class(self)
            provider.register()
        return self

    def use_storage_path(self, path: str) -> None:
        self.storage_path = path

    def get_storage_path(self) -> str:
        return self.storage_path

    def add_providers(self, *providers: Type["Provider"]) -> "Application":
        for provider_class in providers:
            provider = provider_class(self)
            provider.register()
            self.providers.append(provider)

        return self

    # @clean looks like that's not used anymore it's done in Route
    # is it okay ? should not be the application or event the container which holds this info ??
    # def set_controller_locations(self, location):
    #     self._controller_locations = location

    # def get_controller_locations(self, location):
    #     return self._controller_locations

    def get_providers(self) -> List["Provider"]:
        return self.providers

    def __call__(self, *args, **kwargs) -> Iterator:
        return self.response_handler(*args, **kwargs)

    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        # @removed:5.0.0
        if Config.has("application.debug"):
            return bool(Config.get("application.debug"))
        else:
            return env("APP_DEBUG", True)

    def is_dev(self) -> bool:
        """Check if app is running in development mode."""
        return not self.is_running_tests() and os.getenv("APP_ENV") in [
            "development",
            "local",
        ]

    def is_production(self) -> bool:
        """Check if app is running in production mode."""
        return os.getenv("APP_ENV") == "production"

    def is_running_tests(self) -> bool:
        """Check if app is running tests."""

        return "pytest" in sys.modules

    def is_running_in_console(self) -> bool:
        """Check if application is running in console. This is useful to only run some providers
        logic when used in console. We can differentiate if the application is being served or
        if an application command is ran in console."""
        if len(sys.argv) > 1:
            return sys.argv[1] != "serve"
        return True

    def environment(self) -> str:
        """Helper to get current environment."""
        if self.is_running_tests():
            return "testing"
        else:
            return os.getenv("APP_ENV")

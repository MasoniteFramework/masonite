from typing import Any

class Hash:
    def add_driver(self, name: str, driver: Any): ...
    def set_configuration(self, config: dict) -> "Hash": ...
    def get_driver(self, name: str = None) -> Any: ...
    def get_config_options(self, driver: str = None) -> dict: ...
    def make(self, string: str, options: dict = {}, driver: str = None) -> str:
        """Hash a string and return as string based on configured hashing protocol."""
        ...
    def make_bytes(self, string: str, options: dict = {}, driver: str = None) -> bytes:
        """Hash a string and return as bytes based on configured hashing protocol."""
        ...
    def check(
        self,
        plain_string: str,
        hashed_string: str,
        options: dict = {},
        driver: str = None,
    ) -> bool:
        """Verify that a given string matches its hashed version (based on configured hashing protocol)."""
        ...
    def needs_rehash(
        self, hashed_string: str, options: dict = {}, driver: str = None
    ) -> bool:
        """Verify that a given hash needs to be hashed again because parameters for generating
        the hash have changed."""
        ...

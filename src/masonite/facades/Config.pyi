from typing import Any

class Config:
    """Configuration facades to manage Masonite config files."""

    def get(self, key: str, default: None) -> Any:
        """Get given key in config, can use a dotted path."""
        ...
    def set(self, key: str, value: Any) -> None:
        """Override config for given key."""
        ...
    def all(self) -> dict:
        """Get all config object."""
        ...

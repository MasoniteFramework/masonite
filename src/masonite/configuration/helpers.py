from typing import Any
from ..facades import Config


def config(key: str, default: Any = None) -> Any:
    """Get a configuration value by key or default value if key does not exist in configuration
    file. Key can be a dotted path to access nested values."""
    return Config.get(key, default)

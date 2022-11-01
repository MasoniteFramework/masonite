from typing import TYPE_CHECKING, Any

from ..facades import Loader
from ..utils.structures import data
from ..exceptions import InvalidConfigurationLocation, InvalidConfigurationSetup

if TYPE_CHECKING:
    from ..foundation import Application


class Configuration:
    """Configuration manager used to load all configuration files and access configuration
    values."""

    # Foundation configuration keys
    reserved_keys = [
        "application",
        "auth",
        "broadcast",
        "cache",
        "database",
        "filesystem",
        "mail",
        "notification",
        "providers",
        "queue",
        "session",
    ]

    def __init__(self, application: "Application"):
        self.application = application
        self._config: dict = data()

    def load(self) -> None:
        """At boot load configuration from all files and store them in here."""
        config_root = self.application.make("config.location")
        for module_name, module in Loader.get_modules(
            config_root, raise_exception=True
        ).items():
            params = Loader.get_parameters(module)
            for name, value in params.items():
                self._config[f"{module_name}.{name.lower()}"] = value

        # check loaded configuration
        if not self._config.get("application"):
            raise InvalidConfigurationLocation(
                f"Config directory {config_root} does not contain required configuration files."
            )

    def merge_with(self, path: str, external_config: dict) -> None:
        """Merge external config at key with project config at same key. It's especially
        useful in Masonite packages in order to merge the configuration default package with
        the package configuration which can be published in project.

        This functions disallow merging configuration using foundation configuration keys
        (such as 'application').
        """
        if path in self.reserved_keys:
            raise InvalidConfigurationSetup(
                f"{path} is a reserved configuration key name. Please use an other key."
            )
        if isinstance(external_config, str):
            # config is a path and should be loaded
            params = Loader.get_parameters(external_config)
        else:
            params = external_config
        base_config = {name.lower(): value for name, value in params.items()}
        merged_config = {**base_config, **self.get(path, {})}
        self.set(path, merged_config)

    def set(self, path: str, value: Any):
        """Set (or override) a value at the given path (which can be a dotted path)."""
        self._config[path] = value

    def has(self, path: str) -> bool:
        """Check if a configuration value exists at the given path (which can be a dotted path)."""
        return path in self._config

    def all(self) -> dict:
        """Get all configuration values as a dictionary."""
        return self._config

    def get(self, path: str, default: Any = None) -> Any:
        """Get the value at given path or default value if path does not exist in
        configuration file. Path can be a dotted path to access nested values."""
        try:
            config_at_path = self._config[path]
            if isinstance(config_at_path, dict):
                return data(config_at_path)
            else:
                return config_at_path
        except KeyError:
            return default
